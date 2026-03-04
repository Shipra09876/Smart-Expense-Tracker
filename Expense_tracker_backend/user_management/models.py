from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import uuid
from phonenumber_field.modelfields import PhoneNumberField

class MyUserManager(BaseUserManager):
    def create_user(self,email,username,tc,name=None,password=None,password2=None,dob=None):
        if not email:
            raise ValueError("User must have email address")
        
        if not username:
            raise ValueError('User must have an username address')
        
        user=self.model(
            email=self.normalize_email(email),
            username=username,
            name=name,
            tc=tc,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,username,name,tc,dob=None,password=None):
        user=self.create_user(
            email,
            username=username,
            name=name,
            password=password,
            tc=tc,
        )

        user.is_admin=True
        user.save(using=self._db)

        return user
    

class User(AbstractBaseUser):
    email=models.EmailField(verbose_name="Email",max_length=255,unique=True)
    username=models.CharField(max_length=100, null=True, blank=True)
    name=models.CharField(max_length=100)
    phone_no=PhoneNumberField(region='IN')
    profile_picture=models.ImageField(upload_to='chat_media/',null=True,blank=True)
    monthly_income=models.FloatField(blank=True,null=True)
    currency=models.CharField(max_length=10,default='INR')
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    tc=models.BooleanField()
    occupation=models.CharField(max_length=100)
    dob=models.DateField(null=True,blank=True)
    otp=models.CharField(max_length=4,null=True,blank=True)
    created_otp=models.DateField(null=True,blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects=MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username','tc','name']

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    


        