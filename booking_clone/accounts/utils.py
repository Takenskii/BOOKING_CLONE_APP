import uuid
from django.core.mail import send_mail
from django.conf import settings

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