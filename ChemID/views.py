from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login,authenticate
from .forms import RegisterForm, RegisterForm1, RegisterForm2, OTPVerify, reaskEmail, programRegister, loginform, workshop_field
from django.conf import settings
from django.core.mail import send_mail
from .models import Spectator, Transaction
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .OTPSender import send_otp
import cryptocode
from django.utils import timezone
import requests
from django.views.decorators.csrf import csrf_exempt
#todo pip install requests
import uuid
from .billdesk.checksum import Checksum
from .billdesk.gen_message import GetMessage
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
import pandas as pd
import os
import mimetypes
from wsgiref.util import FileWrapper
from django.http import StreamingHttpResponse
import threading
# Create your views here.

from django.contrib.auth.decorators import login_required

def homepage(request):
    return render(request, 'explore.html')


def comingsoon(request):
    return render(request, 'coming soon.html')

@login_required
def download_data(request, program):
    program = eval(program)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(base_dir)
    #return HttpResponse('Hi')
    for i in program:
        querystring = False
        if i == 'All':
            querystring = Spectator.objects.filter(verified=True)
        elif i == 'All events pass':
            if querystring:
                querystring += Spectator.objects.filter(verified=True, is_all_events=True)
            else:
                querystring = Spectator.objects.filter(verified=True, is_all_events=True)
        elif i == 'Ansys':
            if querystring:
                querystring += Spectator.objects.filter(verified=True, is_ansys=True)
            else:
                querystring = Spectator.objects.filter(verified=True, is_ansys=True)
        elif i == 'Python':
            if querystring:
                querystring += Spectator.objects.filter(verified=True, is_python=True)
            else:
                querystring = Spectator.objects.filter(verified=True, is_python=True)
        elif i == 'Matlab':
            if querystring:
                querystring += Spectator.objects.filter(verified=True, is_matlab=True)
            else:
                querystring = Spectator.objects.filter(verified=True, is_matlab=True)
        elif i == 'Aspen':
            if querystring:
                querystring += Spectator.objects.filter(verified=True, is_aspen=True)
            else:
                querystring = Spectator.objects.filter(verified=True, is_aspen=True)
        elif i == 'DWSIM':
            if querystring:
                querystring += Spectator.objects.filter(verified=True, is_dwsim=True)
            else:
                querystring = Spectator.objects.filter(verified=True, is_dwsim=True)
        # if i == 'All':
        #     querystring = Spectator.objects.filter(verified=True)
        # elif i == 'Crash Course':
        #     if querystring:
        #         querystring += Spectator.objects.filter(verified=True, is_workshop=True)
        #     else:
        #         querystring = Spectator.objects.filter(verified=True, is_workshop=True)
    df = pd.DataFrame(list(querystring.values('first_name','last_name','chem_id', 'email','mob_number','is_all_events','is_ansys',
                                              'is_python','is_matlab','is_aspen','is_dwsim','is_iit_madras')))
    #return HttpResponse(df.to_html())
    #data = [[1,2],[3,4]]
    #df = pd.DataFrame(data,columns=['A','B'])
    directory = base_dir+'/static/files'
    file = 'data.xlsx'
    # %%
    if not os.path.exists(directory):
        print("error")
    # %%
    df.to_excel(os.path.join(directory, file))
    chunk_size = 1024
    thefile = os.path.join(directory, file)
    response = StreamingHttpResponse(FileWrapper(open(thefile, 'rb'), chunk_size), content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length'] = os.path.getsize(thefile)
    response['Content-Disposition'] = 'attachment; filename=%s' % file
    #print('end')
    return response

from django.db.models import Count

@login_required
def return_table(request):
    insta = Spectator.objects.filter(source='Instagram')
    insp = insta.filter(is_workshop=True)
    other = Spectator.objects.filter(source='Other')
    op = other.filter(is_workshop=True)
    linkin = Spectator.objects.filter(source='LinkedIn')
    lp = linkin.filter(is_workshop=True)
    d2c = Spectator.objects.filter(source='Dare2Compete')
    dp = d2c.filter(is_workshop=True)
    coll = Spectator.objects.filter(source='College')
    colp = coll.filter(is_workshop=True)
    frn = Spectator.objects.filter(source='Friends')
    fp = frn.filter(is_workshop=True)

    lis = [['Instagram',len(insta),len(insp),len(insta)-len(insp)],['LinkedIn',len(linkin),len(lp),len(linkin)-len(lp)],['D2C',len(d2c),len(dp),len(d2c)-len(dp)],['College',len(coll),len(colp),len(coll)-len(colp)],['Friends',len(frn),len(fp),len(frn)-len(fp)],['Other',len(other),len(op),len(other)-len(op)]]
    #print(lis,'hiiiiiiii')
    if request.method == 'POST':
        form = workshop_field(request.POST)
        if form.is_valid():
            program = form.cleaned_data['program']
            program = [program]
            querystring = False
            #print(program)
            # ("All events pass", "All events pass"),
            # ("Ansys", "Ansys"),
            # ("Python", "Python"),
            # ("SciLab", "SciLab"),
            # ("Matlab", "Matlab"),
            # ("Aspen", "Aspen"),
            # ("DWSIM", "DWSIM")
            for i in program:
                if i=='All':
                    querystring = Spectator.objects.filter(verified=True)
                elif i=='All events pass':
                    if querystring:
                        querystring += Spectator.objects.filter(verified=True, is_all_events=True)
                    else:
                        querystring = Spectator.objects.filter(verified=True, is_all_events=True)
                elif i == 'Ansys':
                    if querystring:
                        querystring += Spectator.objects.filter(verified=True, is_ansys=True)
                    else:
                        querystring = Spectator.objects.filter(verified=True, is_ansys=True)
                elif i == 'Python':
                    if querystring:
                        querystring += Spectator.objects.filter(verified=True, is_python=True)
                    else:
                        querystring = Spectator.objects.filter(verified=True, is_python=True)
                elif i == 'Matlab':
                    if querystring:
                        querystring += Spectator.objects.filter(verified=True, is_matlab=True)
                    else:
                        querystring = Spectator.objects.filter(verified=True, is_matlab=True)
                elif i == 'Aspen':
                    if querystring:
                        querystring += Spectator.objects.filter(verified=True, is_aspen=True)
                    else:
                        querystring = Spectator.objects.filter(verified=True, is_aspen=True)
                elif i == 'DWSIM':
                    if querystring:
                        querystring += Spectator.objects.filter(verified=True, is_dwsim=True)
                    else:
                        querystring = Spectator.objects.filter(verified=True, is_dwsim=True)

                     # render(request, 'signup.html', {'form': form, 'msg':'U need to verify ur email'})
            return render(request, 'Tabledisplay.html', {'form': form,'d':querystring,'prog':str(program),'dataset':lis})
        else:
            form = workshop_field()
            return render(request, 'Tabledisplay.html', {'form': form,'dataset':lis})
    form = workshop_field()
    return render(request, 'Tabledisplay.html', {'form': form,'dataset':lis})

def login_view(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('secretpage')
                else:
                    return HttpResponse('Please provide correct creds')#render(request, 'signup.html', {'form': form, 'msg':'U need to verify ur email'})
            else:
                form = loginform()
                return HttpResponse('Please provide correct creds')
    form = loginform()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


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
            src = form2.cleaned_data['source']

            email_otp = send_otp([email], f_name, 'DNE')


            Spectator.objects.create(first_name=f_name, last_name=l_name, gender=gen, email=email, mob_number=mob_number, alt_mob_number=alt_phone_number, department=departmen
                                     , address=address, zipcode=zipcode, state=stat, college=college, program=proga, year=yea, email_otp=email_otp,source=src, verified=False)

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
            if e_otp == f"{email_otp:06d}":
                usr_details.verified = True
                usr_details.save()
                error = 'Successfully Verified!!! You will receive your CHES ID on your Email ID'
                uid = usr_details.chem_id
                name = usr_details.first_name
                subject = ['Ches ID', uid]
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
                subject = ['Ches ID', uid]
                recipient_list = [email]
                usr_name = usr_details.first_name + ' '+usr_details.last_name
                college = usr_details.college
                number = usr_details.mob_number
                message = [usr_name, email, college, number]
                mailer(recipient_list, name, 'mail_template.html', subject, message)
                error = "Ches ID has been sent to your mail ID"
                return render(request, 'resend2.html', {'error': error, 'form': form, 'typ': 'success'})
    else:
        form = reaskEmail()
    error = 'We will try our best to help you out! Enter the mail ID with which you registered'
    return render(request, 'resend2.html', {'error': error, 'form': form, 'typ': 'primary'})


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkiitm(request):
    if request.is_ajax and request.method == "POST":
        email = request.POST.get('email', None)
        cid = request.POST.get('chem_id', None)
        user = Spectator.objects.filter(chem_id=cid)

        if user and user[0].email==email:
            if user[0].is_iit_madras:
                reply = 1
            else:
                reply = 2

        else:
            reply = -1
        print(len(user))

        data = {
            'status': reply
        }
        return JsonResponse(data)



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
                mail = usr_details.email
                fname = usr_details.first_name
                mnumber = usr_details.mob_number
                while True:
                    oid = get_order_id(chem_id)
                    #print(oid)
                    trans = Transaction.objects.filter(order_id=oid)
                    if not trans:
                        break
                choices = form.cleaned_data['programs']
                print(choices,'choice')
                if "Python" in choices and "SciLab" in choices:
                    error = "Register either for Python or for SciLab."
                    return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                elif "Python" in choices and "Ansys" in choices:
                    error = "Register either for Python or for Ansys."
                    return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                # elif "Aspen" in choices and "DWSIM" in choices:
                #     error = "Register either for DWSIM or for Aspen."
                #     return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
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
                        if usr_details.is_python:
                            error = f"You have already registered for Python and you can register either for python or ansys.Contact us if you have any issues"
                            return render(request, 'paymentspage.html',
                                          {'error': error, 'form': form, 'typ': 'warning'})
                        amount+=settings.AMT_ANSYS
                    elif i=='Python':
                        if usr_details.is_python:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        if usr_details.is_scilab:
                            error = f"You have already registered for SciLab and you can register either for python or scilab.Contact us if you have any issues"
                            return render(request, 'paymentspage.html',
                                          {'error': error, 'form': form, 'typ': 'warning'})
                        if usr_details.is_ansys:
                            error = f"You have already registered for Ansys and you can register either for python or ansys.Contact us if you have any issues"
                            return render(request, 'paymentspage.html',
                                          {'error': error, 'form': form, 'typ': 'warning'})
                        amount+=settings.AMT_PYTHON
                    elif i=='SciLab':
                        if usr_details.is_scilab:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        if usr_details.is_python:
                            error = f"You have already registered for Python and you can register either for python or scilab.Contact us if you have any issues"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        amount+=settings.AMT_SCILAB
                    elif i=='Matlab':
                        if usr_details.is_matlab:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.AMT_MATLAB
                    elif i=='Aspen':
                        if usr_details.is_aspen:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_dwsim:
                        #     error = f"You have already registered for DWSIM and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.AMT_ASPEN
                    elif i=='DWSIM':
                        if usr_details.is_dwsim:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.AMT_DWSIM
                    elif i=='MSME':
                        if usr_details.is_msme:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.AMT_MSME

                    elif i=='workshop_prog':
                        if usr_details.is_workshop:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        if usr_details.is_iit_madras:
                            amount += settings.AMT_WORKSHOP_IITM
                        else:
                            amount += settings.AMT_WORKSHOP_NOIITM
                    elif i=='CHES Fee (2020 Batch)':
                        if usr_details.is_workshop:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.CHES_FEE2020
                    elif i=='CHES Fee (2021 Batch)':
                        if usr_details.is_workshop:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.CHES_FEE2021
                    elif i=='T-Shirt':
                        if usr_details.is_workshop:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.TSHIRT
                    elif i=='T-Shirt (Combo)':
                        if usr_details.is_workshop:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.TSHIRTCOMBO
                    elif i=='T-Shirt (Cusomised)':
                        if usr_details.is_workshop:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.TSHIRTCUS
                    elif i=='T-Shirt (Combo Cusomised)':
                        if usr_details.is_workshop:
                            error = f"You have already registered for {i}. We don't charge twice"
                            return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'warning'})
                        # if usr_details.is_aspen:
                        #     error = f"You have already registered for Aspen and you can register either for DWSIM or Aspen.Contact us if you have any issues"
                        #     return render(request, 'paymentspage.html',
                        #                   {'error': error, 'form': form, 'typ': 'warning'})
                        amount += settings.TSHIRTCOMBOCUS

                #print(amount)
                msg = GetMessage().message(oid, amount, chem_id, mail, fname, mnumber)
                #print(msg)
                Transaction.objects.create(owner=usr_details, order_id=oid, email=usr_details.email, amount_initiated=amount, status='PENDING', registered_for=choices, log=str([msg]), txn_date=timezone.localtime(timezone.now()))
                #return HttpResponse('Coming soon')
                return render(request, 'paymentProcess.html', {'msg': msg, 'url': settings.BILL_URL})
                #print(settings.BILL_URL)
                #resp = requests.post(settings.BILL_URL, data=msg)
                #print(resp.status_code)
                #print(resp.content)
                #print(resp.text)
            else:
                #print('not found')
                error = "Given Ches ID doesn't exist OR the entered Ches ID and email ID don't match with the data stored in Database"
                return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'danger'})
        error = ''
        return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'empty'})
    form = programRegister()
    error = ''
    firsttiem = 'fs'
    return render(request, 'paymentspage.html', {'error': error, 'form': form, 'typ': 'empty', 'fs':firsttiem})


def findNthOccur(string, ch, N):
    occur = 0

    # Loop to find the Nth
    # occurence of the character
    for i in range(len(string)):
        if (string[i] == ch):
            occur += 1

        if (occur == N):
            return i

    return -1

def get_mode(s):
    if s == '01':
        return 'Netbanking'
    elif s == '02':
        return 'Credit Card'
    elif s == '03':
        return 'Debit Card'
    elif s == '04':
        return 'Cash Card'
    elif s == '05':
        return 'Mobile Wallet'
    elif s == '06':
        return 'IMPS'
    elif s == '07':
        return 'Reward Points'
    elif s == '08':
        return 'Rupay'
    elif s == '09':
        return 'Others'
    elif s == '10':
        return 'UPI'

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
        pipeind7 = findNthOccur(response, '|', 7)
        pipeind8 = findNthOccur(response, '|', 8)
        pipeind9 = findNthOccur(response, '|', 9)
        pipeind10 = findNthOccur(response, '|', 10)
        pipeind12 = findNthOccur(response, '|', 13)
        pipeind13 = findNthOccur(response, '|', 14)
        pipeind14 = findNthOccur(response, '|', 15)
        mid = response[:pipeind1]
        oid = response[pipeind1+1:pipeind2]
        txnid = response[pipeind2+1:pipeind3]
        amnt = response[pipeind4+1:pipeind5]
        tstat = response[pipeind13+1:pipeind14]
        dnt = response[pipeind12 + 1:pipeind13]
        mode = response[pipeind7 + 1:pipeind8]
        mode = get_mode(mode)



        if valid_payment and mid == settings.MID:
            transac = Transaction.objects.filter(order_id=oid)
            if transac:
                transac = transac[0]
                #transac.txn_id = txnid
                if tstat == '0300' and transac.amount_initiated==float(amnt):
                    #transac.status = 'SUCCESS'
                    chem_id = transac.owner.chem_id
                    reg_for = eval(transac.registered_for)
                    usr_details = Spectator.objects.filter(chem_id=chem_id)[0]
                    # for i in reg_for:
                    #     if i == 'All events pass':
                    #         usr_details.is_all_events = True
                    #     elif i == 'Ansys':
                    #         usr_details.is_ansys = True
                    #     elif i == 'Python':
                    #         usr_details.is_python = True
                    #     elif i == 'SciLab':
                    #         usr_details.is_scilab = True
                    #     elif i == 'Matlab':
                    #         usr_details.is_matlab = True
                    #usr_details.save()
                    #transac.was_success = True
                    typ = 'success'
                    msgs = ['Success','Payment Succesfull', reg_for]
                elif tstat == '0300' and transac.amount_initiated!=amnt:
                    reg_for = eval(transac.registered_for)
                    #transac.status = 'AMOUNT Tampered'
                    #transac.was_success = False
                    msgs = ['Failed', 'Payment declined! Looked liked someone tried tampering your payment',reg_for]
                    typ='danger'
                elif tstat == '0002':
                    #transac.status = "WAITING"
                    reg_for = eval(transac.registered_for)
                    msgs = ['Failed', 'Billdesk is waiting for the trasaction status from your bank. Will update you as soon as we have any response',reg_for]
                    typ = 'info'
                elif tstat != '0300':
                    if tstat == '0399':
                        sm = 'Invalid Authentication at Bank'
                    elif tstat == 'NA':
                        sm = 'Invalid Input in the Request Message'
                    elif tstat =='0001':
                        sm = 'error at billdesk'
                    else:
                        sm = 'Payment Failed'
                    #transac.status = "FAILED"
                    reg_for = eval(transac.registered_for)
                    msgs = ['Failed', sm, reg_for]
                    typ = 'danger'
                transac.log += str([response])
                transac.ru_date = timezone.localtime(timezone.now())
                transac.save()
                return render(request, 'afterPayment.html', {'error': msgs, 'typ':typ, 'txnid':txnid, 'date':dnt, 'amnt': amnt, 'mode':mode})
            else:
                return HttpResponse('Bad Request')
        else:
            transac = Transaction.objects.filter(order_id=oid)
            if transac:
                transac = transac[0]
                #transac.txn_id = txnid
                #transac.status = 'CHECKSUM verification failed'
                transac.log += str([response])
                transac.ru_date = timezone.localtime(timezone.now())
                reg_for = eval(transac.registered_for)
                transac.save()
                msgs = ['Failed','Payment declined! Looked liked someone tried tampering your payment', reg_for]
                return render(request, 'afterPayment.html', {'error': msgs, 'typ': 'danger', 'txnid':txnid, 'date':dnt, 'amnt': amnt, 'mode':mode})
            else:
                return HttpResponse('Bad Request')
    else:
        return HttpResponse('Bad Request')


@csrf_exempt
def server_to_server(request):
    if request.method=='POST':
        response = request.POST
        response = response['msg'].strip('()')
        response = response.strip('\n')
        #print(response)
        valid_payment = Checksum().verify_checksum(response)
        pipeind1 = findNthOccur(response, '|', 1)
        pipeind2 = findNthOccur(response, '|', 2)
        pipeind3 = findNthOccur(response, '|', 3)
        pipeind4 = findNthOccur(response, '|', 4)
        pipeind5 = findNthOccur(response, '|', 5)
        pipeind13 = findNthOccur(response, '|', 14)
        pipeind14 = findNthOccur(response, '|', 15)
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
                        elif i == 'CHES Fee (2020 Batch)':
                            usr_details.is_ches2020 = True
                        elif i == 'CHES Fee (2021 Batch)':
                            usr_details.is_ches2021 = True
                        elif i == 'T-Shirt':
                            usr_details.is_tshirt = True
                        elif i == 'T-Shirt (Combo)':
                            usr_details.is_tshirtcombo = True
                        elif i == 'T-Shirt (Cusomised)':
                            usr_details.is_tshirtcus = True
                        elif i == 'T-Shirt (Combo Cusomised)':
                            usr_details.is_tshirtcombocus = True
                    usr_details.save()
                    transac.was_success = True
                transac.log += str([response])
                transac.s2s_date = timezone.localtime(timezone.now())
                transac.save()
   