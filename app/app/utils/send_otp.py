from django.core.mail import send_mail
import random
import string

def generate_otp():
    otp = ''.join(random.choices(string.digits, k=6))  # Generate a 6-digit OTP
    return otp

def send_otp_email(email, otp):
    subject = 'Your OTP Verification Code'
    message = f'Your OTP is: {otp}'
    from_email = 'feridabd37@example.com'
    send_mail(subject, message, from_email, [email])