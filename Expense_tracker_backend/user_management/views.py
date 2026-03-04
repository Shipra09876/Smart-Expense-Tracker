from django.shortcuts import render
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
import json
import logging
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from user_management.serializers import *
from django.contrib.auth import authenticate
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.utils import *
from django.utils import timezone
from user_management.otp_utils import *
from datetime import timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def get_token_for_user(user):
    refresh=RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }

class UserRegister(APIView):
    permission_classes=[AllowAny]
    renderer_classes=[JSONRenderer]

    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token=get_token_for_user(user)
            
            return Response({
                'token':token,
                "msg":"Register successfully",
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes=[AllowAny]
    renderer_classes=[JSONRenderer]

    def post(self,request,format=None):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            email=serializer.data.get('email')
            password=serializer.data.get('password')
            user=authenticate(email=email,password=password)

            if user is not None:
                token=get_token_for_user(user)
                user_data=LoginSerializer(user).data
                return Response({'token':token, "msg":"Login successfully"},status=status.HTTP_200_OK)
            else:
                return Response({'error':{'non_field_errors':['email and password are not Valid']}},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'errors':serializer.errors,
            "msg":"Login unsuccessfull"
        },status=status.HTTP_400_BAD_REQUEST)
    

class UserProfile(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def get(self,request):
        serializer=ProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class UserLogout(APIView):
    permission_classes=[IsAuthenticated]
    renderer_classes=[JSONRenderer]

    def post(self,request,format=None):
        serializer=LogoutSerializer(data=request.data)

        if serializer.is_valid():
            refresh_token=serializer.validated_data['refresh']

            try:
                token=RefreshToken(refresh_token)
                token.blacklist()
                return Response({"msg":"Logout successfully"},status=status.HTTP_200_OK)
            
            except Exception as e:
                logger.warning("Logout unsuccessful")
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ChangePassword(APIView):
    renderer_classes=[JSONRenderer]
    permission_classes=[IsAuthenticated]

    def post(self,request,format=None):
        serializer=ChangePasswordSerializer(data=request.data,context={'user':request.user})

        if serializer.is_valid():
            return Response({
                "msg":"Password change successfully",
            },status=status.HTTP_200_OK)
        
        return Response({
            serializer.errors,
        },status=status.HTTP_400_BAD_REQUEST)

class SendResetPasswordEmail(APIView):
    renderer_classes=[JSONRenderer]
    permission_classes=[AllowAny]

    def post(self,request,format=None):
        serializer=SendResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "msg":"email send successfully , check your email"
            },status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ResetPassword(APIView):
    renderer_classes=[JSONRenderer]
    permission_classes=[AllowAny]

    def post(self,request,uid,token,format=None):
        serializer=ResetPasswordSerializer(data=request.data,context={'uid':uid,'token':token})
        
        if serializer.is_valid():
            return Response({
                "msg":"Password Reset Successfully"
            },status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
 

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/"
    client_class = OAuth2Client



class FirstLogin(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')

        user=authenticate(email=email,password=password)
        if user:
            otp=generate_otp()
            user.otp=otp
            user.created_otp=timezone.now()
            user.save()
        
            util.send_otp_email(user.email,otp)
            print(f"{otp}")
            return Response({"msg":"OTP sent successfully to your email"},status=status.HTTP_200_OK)
    
        return Response({"msg":"Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)
    
class VerifyOTP(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        email=request.data.get('email')
        otp=request.data.get('otp')
        print(f"otp:{otp}")

        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"Msg":"User doesn't exist"},status=status.HTTP_404_NOT_FOUND)
        
        print("user otp",user.otp)
        if str(user.otp).strip()!=str(otp).strip():
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        print(f"created otp: {user.created_otp}")
        if user.created_otp and isinstance(user.created_otp, timezone.datetime):
            if timezone.now() > user.created_otp + timedelta(minutes=5):
                return Response({"Error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)


        from rest_framework_simplejwt.tokens import RefreshToken
        refresh=RefreshToken.for_user(user)

        # clean otp
        user.otp=None
        user.created_otp=None
        user.save()

        return Response({
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        },status=status.HTTP_200_OK)
    
