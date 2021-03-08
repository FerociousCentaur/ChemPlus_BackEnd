from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login,authenticate
from .forms import RegisterForm, RegisterForm1, RegisterForm2, OTPVerify, reaskEmail, programRegister
from django.conf import settings
from django.core.mail import send_mail
from .models import Spectator, Transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .OTPSender import send_otp
import cryptocode
import requests
from django.views.decorators.csrf import csrf_exempt
#todo pip install requests
import uuid
from .billdesk.checksum import Checksum
from .billdesk.gen_message import GetMessage


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

    return render(response, 'signup2.html', {"form": form, "form1": form1, "form2": form2})#signup.html

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
            if e_otp == str(email_otp):
                usr_details.verified = True
                usr_details.save()
                error = 'Successfully Verified!!! You will receive your CHEM+ ID on your Email ID'
                uid = usr_details.chem_id
                name = usr_details.first_name
                subject = ['ChemPlus ID', uid]
                recipient_list = [email]
                usr_name = usr_details.first_name+' '+usr_details.last_name
                college = usr_details.college
                number = usr_details.mob_number
                message = [usr_name,email,college,number]
                mailer(recipient_list, name, 'mail_template.html', subject, message)
                return render(request,'signupverify2.html',{'error': error, 'form':form, 'typ': 'success'})
            else:
                error = "OTP does not match!! Retry"
                return render(request,'signupverify2.html',{'error':error, 'form': form, 'typ': 'warning'})
    else:
        form = OTPVerify()
        error = 'OTP has been sent to your registered email ID.Please enter the OTP to verify your email ID'
    return render(request,'signupverify2.html', {'error': error, 'form': form, 'typ': 'success'})

def resendOTP(request):
    if request.method == "POST":
        form = reaskEmail(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            usr_details = Spectator.objects.filter(email=email)
            if not usr_details:
                error = "Looks like you have not signed up! Try signing up again"
                return render(request, 'resend2.html', {'error': error, 'form': form, 'typ': 'info'})
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
                usr_name = usr_details.first_name + ' '+usr_details.last_name
                college = usr_details.college
                number = usr_details.mob_number
                message = [usr_name, email, college, number]
                mailer(recipient_list, name, 'mail_template.html', subject, message)
                error = "ChemPlus ID has been sent to your mail ID"
                return render(request, 'resend2.html', {'error': error, 'form': form, 'typ': 'success'})
    else:
        form = reaskEmail()
    error = 'We will try our best to help you out! Enter the mail ID with which you registered'
    return render(request, 'resend2.html', {'error': error, 'form': form, 'typ': 'primary'})


def get_order_id(chem_id):
    return chem_id+str(uuid.uuid4())[:8]

# payment handling

def payment_request(request):
    if request.method == 'POST':
        form = programRegister(request.POST)
        if form.is_valid():
            amount = 0
            chem_id = form.cleaned_data['chem_id']
            usr_details = Spectator.objects.filter(chem_id=chem_id)
            if usr_details and usr_details[0].email == form.cleaned_data['email']:
                usr_details = usr_details[0]
                while True:
                    oid = get_order_id(chem_id)
                    #print(oid)
                    trans = Transaction.objects.filter(order_id=oid)
                    if not trans:
                        break
                choices = form.cleaned_data['programs']
                if "Python" in choices and "SciLab" in choices:
                    error = "Register either for Python or for SciLab."
                    return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                #print(choices)
                for i in choices:
                    if i=='All events pass':
                        if usr_details.is_all_events:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        amount+=settings.AMT_ALL_EVENTS
                    elif i=='Ansys':
                        if usr_details.is_ansys:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        amount+=settings.AMT_ANSYS
                    elif i=='Python':
                        if usr_details.is_python:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        if usr_details.is_scilab:
                            error = f"You have already registered for SciLab and you can register either for python or scilab.Contact us if you have any issues"
                            return render(request, 'paymentspage.html',
                                          {'error': error, 'form': form, 'typ': 'warning'})
                        amount+=settings.AMT_PYTHON
                    elif i=='SciLab':
                        if usr_details.is_scilab:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        amount+=settings.AMT_SCILAB
                    elif i=='Matlab':
                        if usr_details.is_matlab:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.AMT_MATLAB
                #print(amount)
                msg = GetMessage().message(oid, amount)
                #print(msg)
                Transaction.objects.create(owner=usr_details, order_id=oid, email=usr_details.email, amount_initiated=amount, status='PENDING', registered_for=choices, log=str([msg]))
                return render(request, 'paymentProcess.html', {'msg': msg, 'url': settings.BILL_URL})
                #print(settings.BILL_URL)
                #resp = requests.post(settings.BILL_URL, data=msg)
                #print(resp.status_code)
                #print(resp.content)
                #print(resp.text)
            else:
                #print('not found')
                error = "Given Chemplus ID doesn't exist OR the entered Chemplus ID and email ID don't match with the data stored in Database"
                return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'danger'})
        error = ''
        return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'empty'})
    form = programRegister()
    error = ''
    return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'empty'})


def findNthOccur(string, ch, N):
    occur = 0;

    # Loop to find the Nth
    # occurence of the character
    for i in range(len(string)):
        if (string[i] == ch):
            occur += 1;

        if (occur == N):
            return i;

    return -1;


#findnth('foobarfobar akfjfoobar afskjdf foobar', 'foobar', 2)



@csrf_exempt
def handleResponse(request):
    if request.method=='POST':
        response = request.POST
        response = response['msg'].strip('()')
        #print(response)
        valid_payment = Checksum().verify_checksum(response)
        pipeind1 = findNthOccur(response, '|', 1)
        pipeind2 = findNthOccur(response, '|', 2)
        pipeind3 = findNthOccur(response, '|', 3)
        pipeind4 = findNthOccur(response, '|', 4)
        pipeind5 = findNthOccur(response, '|', 5)
        pipeind13 = findNthOccur(response, '|', 13)
        pipeind14 = findNthOccur(response, '|', 14)
        mid = response[:pipeind1]
        oid = response[pipeind1+1:pipeind2]
        txnid = response[pipeind2+1:pipeind3]
        amnt = response[pipeind4+1:pipeind5]
        tstat = response[pipeind13+1:pipeind14]

        if valid_payment and mid == settings.MID:
            transac = Transaction.objects.filter(order_id=oid)
            if transac:
                transac = transac[0]
                transac.txn_id = txnid
                if tstat == '0300' and transac.amount_initiated==float(amnt):
                    transac.status = 'SUCCESS'
                    chem_id = transac.owner.chem_id
                    reg_for = eval(transac.registered_for)
                    usr_details = Spectator.objects.filter(chem_id=chem_id)[0]
                    for i in reg_for:
                        if i == 'All events pass':
                            usr_details.is_all_events = True
                        elif i == 'Ansys':
                            usr_details.is_ansys = True
                        elif i == 'Python':
                            usr_details.is_python = True
                        elif i == 'SciLab':
                            usr_details.is_scilab = True
                        elif i == 'Matlab':
                            usr_details.is_matlab = True
                    usr_details.save()
                    transac.was_success = True
                    typ = 'success'
                    msgs = 'Payment Succesfull'
                elif tstat == '0300' and transac.amount_initiated!=amnt:
                    transac.status = 'AMOUNT Tampered'
                    transac.was_success = False
                    msgs = 'Payment declined! Looked liked someone tried tampering your payment'
                    typ='danger'
                elif tstat != '0300':
                    transac.status = "FAILED"
                    msgs = 'Payment Failed'
                    typ = 'danger'
                transac.log += response
                transac.save()
                msgs = 'Payment declined! Looked liked someone tried tampering your payment'
                return render('request', 'afterPayment.html', {'error': msgs, 'typ':typ, 'txnid':txnid})
            else:
                return HttpResponse('Bad Request')
        else:
            transac = Transaction.objects.filter(order_id=oid)
            if transac:
                transac = transac[0]
                transac.txn_id = txnid
                transac.status = 'CHECKSUM verification failed'
                transac.log += str([response])
                transac.save()
                msgs = 'Payment declined! Looked liked someone tried tampering your payment'
                return render('request', 'afterPayment.html', {'error': msgs, 'typ': 'danger', 'txnid':txnid})
            else:
                return HttpResponse('Bad Request')
    else:
        return HttpResponse('Bad Request')
