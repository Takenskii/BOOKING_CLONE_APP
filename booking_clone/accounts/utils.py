import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.utils.text import slugify
from .models import Hotel


def generateRandomToken():
    return str(uuid.uuid4())

# for sending email token
def sendEmailToken(email, token):
    subject = "Verify Your Email Address"
    verification_url = f"http://127.0.0.1:8000/accounts/verify-account/{token}"
    message = f"Hi, please verify your email account by clicking this link: {verification_url}"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )   

# for sending otp

def sendOTPtoEmail(email, otp):
    subject = "OTP for account login"
    message = f"""Hi, use this OTP to login {otp} """

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )   

def generateSlug(hotel_name):
    slug = f"{slugify(hotel_name)}-" + str(uuid.uuid4()).split('-')[0]
    if Hotel.objects.filter(hotel_slug=slug).exists():
        return generateSlug(hotel_name)
    return slug