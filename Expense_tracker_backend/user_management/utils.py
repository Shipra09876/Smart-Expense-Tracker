from django.conf import settings
from django.core.mail import send_mail,EmailMessage
import uuid
import random

class util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['subject'],
            body=data['body'],
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[data['to_email']]
        )

        email.send()
    
    def send_otp_email(user_email,otp):
        subject="YOUR 2FA Authentication"
        message=f"YOUR OTP IS {otp} , WILL BE EXPIRED IN 5 MIN"
        from_email=settings.DEFAULT_FROM_EMAIL
        send_mail(subject,message,from_email,[user_email])
        

    



