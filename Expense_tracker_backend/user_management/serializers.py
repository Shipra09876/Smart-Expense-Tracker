from rest_framework import serializers
from user_management.models import User
from django.contrib.auth import get_user_model
from xml.dom import VALIDATION_ERR
import uuid
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import util
from dj_rest_auth.registration.serializers import RegisterSerializer

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['email','username','name','phone_no','password','password2','tc','dob','occupation','profile_picture','monthly_income','currency']

        extra_kwargs={
            'password':{'write_only':True}
        }

    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')

        if password!=password2:
            raise serializers.ValidationError("password and confirm password are not same")
        return attrs
    
    def create(self,validated_data):
        validated_data.pop('password2')
        password=validated_data.pop('password')
        user=User(**validated_data)
        user.set_password(password)
        user.save()

        return user
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)

    class Meta:
        model=User
        fields=['email','password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['email','username','name','dob','occupation','profile_picture','monthly_income','currency']
        

class LogoutSerializer(serializers.Serializer):
    refresh=serializers.CharField()

    class Meta:
        model=User
        fields=['refresh']

    def validate(self,attrs):
        refresh=attrs.get('refresh')
    
        if not refresh:
            raise serializers.ValidationError("Refresh token is required")

        return attrs
        

class ChangePasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=100,min_length=4,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=100,min_length=4,style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['password','password2']
    
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')

        if password!=password2:
            raise serializers.ValidationError("password and confirm password are not same")
        
        user.set_password(password)
        user.save()
        return attrs

class SendResetPasswordEmailSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=100)

    class Meta:
        model=User
        fields=['email']
    
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user) 
            link='http://localhost:3000/reset_password/'+uid+'/'+token

            body='Click following to reset password'+link
            data={
                'subject':"Reset Password Email",
                'body':body,
                'to_email':user.email
            }

            util.send_email(data)
            return attrs
        else:
            raise VALIDATION_ERR("You are not registered user")


class ResetPasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=100,min_length=4,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=100,min_length=4,style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['password','password2']

    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uid=self.context.get('uid')
            token=self.context.get('token')

            if password!=password2:
                raise ValueError("password and confirm password are not same")
            
            id=smart_str(urlsafe_base64_decode(uid))
            user=User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                raise VALIDATION_ERR("Token is not valid or expired")
            
            user.set_password(password)
            user.save()
            return attrs
        
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise VALIDATION_ERR("Token is not valid or expired")
