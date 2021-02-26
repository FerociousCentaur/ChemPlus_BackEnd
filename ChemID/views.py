from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login,authenticate
from .forms import RegisterForm, RegisterForm1, RegisterForm2, OTPVerify, reaskEmail
from django.conf import settings
from django.core.mail import send_mail
from .models import Spectator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .OTPSender import send_otp
import cryptocode

import threading
# Create your views here.





def signup(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        form1 = RegisterForm1(response.POST)
        form2 = RegisterForm2(response.POST)
        if all([form.is_valid(), form1.is_valid(), form2.is_valid()]):
            f_name = form.cleaned_data['f_name']
            l_name = form.cleaned_data['l_name']
            gen = form.cleaned_data['gen']

            email = form1.cleaned_data['email']
            mob_number = form1.cleaned_data['mob_number']
            alt_phone_number = form1.cleaned_data['alt_phone_number']
            address = form1.cleaned_data['address']
            zipcode = form1.cleaned_data['zipcode']

            stat = form2.cleaned_data['stat']
            college = form2.cleaned_data['college']
            departmen = form2.cleaned_data['departmen']
            proga = form2.cleaned_data['progra']
            yea = form2.cleaned_data['yea']

            email_otp = send_otp([email], f_name, 'DNE')


            Spectator.objects.create(first_name=f_name, last_name=l_name, gender=gen, email=email, mob_number=mob_number, alt_mob_number=alt_phone_number, department=departmen
                                     ,address=address, zipcode=zipcode, state=stat, college=college, program=proga, year=yea, email_otp=email_otp, verified=False)

            # usr_details = Spectator.objects.filter(email=email)[0]
            # uid = usr_details.chem_id
            # name = usr_details.first_name
            # subject = ['ChemPlus ID',uid]
            # recipient_list = [email]
            # message=''
            # mailer(recipient_list, name, 'mail_template.html', subject, message)
            #send_mail(subject, message, email_from, recipient_list)
            cypt_mail = cryptocode.encrypt(email, "this is the encrypted email")
            return redirect(f'/signupverify/{cypt_mail}')
    else:
        form = RegisterForm()
        form1 = RegisterForm1()
        form2 = RegisterForm2()

    return render(response, 'signup.html', {"form": form, "form1": form1, "form2": form2})

def mailer(receiver,name,path,sub,msg):


    subject, from_email, to = sub[0], settings.EMAIL_HOST_USER, receiver

    html_content = render_to_string(path, {'Pname': name, 'uid': sub[1], 'message': msg})  # render with dynamic value
    text_content = strip_tags(html_content)  # Strip the html tag. So people can see the pure text at least.

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def Verifier(request,crypt_mail):
    if request.method == "POST":
        form = OTPVerify(request.POST)
        if form.is_valid():
            email = cryptocode.decrypt(crypt_mail, "this is the encrypted email")
            e_otp = form.cleaned_data['email_otp']
            usr_details = Spectator.objects.filter(email=email)[0]
            email_otp = usr_details.email_otp
            if int(e_otp) == email_otp:
                usr_details.verified = True
                usr_details.save()
                error = 'Successfully Verified!!! You will receive your CHEM+ ID on your Email ID'
                uid = usr_details.chem_id
                name = usr_details.first_name
                subject = ['ChemPlus ID', uid]
                recipient_list = [email]
                message = ''
                mailer(recipient_list, name, 'mail_template.html', subject, message)
                return render(request,'signupverify.html',{'error': error, 'form':form})
            else:
                error = "OTP does not match!! Retry"
                return render(request,'signupVerify.html',{'error':error, 'form': form})
    else:
        form = OTPVerify()
        error = 'OTP has been sent to your registered email ID.You have 15 minutes to verify!'
    return render(request,'signupverify.html', {'error': error, 'form': form})

def resendOTP(request):
    if request.method == "POST":
        form = reaskEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            usr_details = Spectator.objects.filter(email=email)
            if not usr_details:
                error = "Looks like you have not signed up! Try signing up again"
                return render(request, 'resend.html', {'error': error, 'form': form})
            usr_details = usr_details[0]
            if not usr_details.verified:
                name = usr_details.first_name
                send_otp([email], name, 'E')
                cypt_mail = cryptocode.encrypt(email, "this is the encrypted email")
                return redirect(f'/signupverify/{cypt_mail}')
            elif usr_details.verified:
                uid = usr_details.chem_id
                name = usr_details.first_name
                subject = ['ChemPlus ID', uid]
                recipient_list = [email]
                message = ''
                mailer(recipient_list, name, 'mail_template.html', subject, message)
                return HttpResponse('ChemPlus ID has been sent to your mail ID')
    else:
        form = reaskEmail()
    error = 'We will try our best to help you out! Enter the mail ID with which you registered'
    return render(request, 'resend.html', {'error': error, 'form': form})

