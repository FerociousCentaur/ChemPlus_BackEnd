# import library
import math, random
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Spectator

# function to generate OTP
def generateOTP():
    # Declare a digits variable
    # which stores all digits
    digits = "123456789"
    OTP = ""

    # length of password can be chaged
    # by changing value in range
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]

    return OTP

def send_otp(email, name, check):
    subject = 'Email Verification OTP'
    from_email, to = settings.EMAIL_HOST_USER, email
    msg=''
    if check== 'DNE':
        otp = generateOTP()
    else:
        usr = Spectator.objects.get(email=email[0])
        otp = usr.email_otp
    html_content = render_to_string('otp.html', {'name': name, 'otp': otp, 'message': msg})  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return otp