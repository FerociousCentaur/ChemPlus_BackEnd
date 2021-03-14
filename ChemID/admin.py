from django.contrib import admin
from .models import Spectator, BroadCast_Email, Transaction
# Register your models here.
from django.db import models
admin.site.register(Spectator)
admin.site.register(Transaction)
#admin.site.register(Product)
from django.contrib import admin
from django.utils.safestring import mark_safe
import threading
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import (send_mail, BadHeaderError, EmailMessage)
from django.contrib.auth.models import User

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(self.subject, self.html_content, settings.EMAIL_HOST_USER, self.recipient_list)
        msg.content_subtype = "html"
        try:
            msg.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

class BroadCast_Email_Admin(admin.ModelAdmin):
    model = BroadCast_Email

    def submit_email(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Spectator.objects.filter(verified=True)] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email.short_description = 'Submit BroadCast (1 Select Only)'
    submit_email.allow_tags = True

    def submit_email_allevents(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Spectator.objects.filter(verified=True, is_all_events=True)] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email_allevents.short_description = 'Submit BroadCast All events'
    submit_email_allevents.allow_tags = True

    def submit_email_ansys(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Spectator.objects.filter(verified=True, is_ansys=True)] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email_ansys.short_description = 'Submit BroadCast Ansys'
    submit_email_ansys.allow_tags = True

    def submit_email_python(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Spectator.objects.filter(verified=True, is_python=True)] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email_python.short_description = 'Submit BroadCast Python'
    submit_email_python.allow_tags = True

    def submit_email_scilab(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Spectator.objects.filter(verified=True, is_scilab=True)] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email_scilab.short_description = 'Submit BroadCast SciLab'
    submit_email_scilab.allow_tags = True

    def submit_email_matlab(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Spectator.objects.filter(verified=True, is_matlab=True)] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email_matlab.short_description = 'Submit BroadCast Matlab'
    submit_email_matlab.allow_tags = True

    def submit_email_aspen(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Spectator.objects.filter(verified=True, is_aspen=True)] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email_matlab.short_description = 'Submit BroadCast Aspen'
    submit_email_matlab.allow_tags = True

    def submit_email_dwsim(self, request, obj): #`obj` is queryset, so there we only use first selection, exacly obj[0]
        list_email_user = [ p.email for p in Spectator.objects.filter(verified=True, is_dwsim=True)] #: if p.email != settings.EMAIL_HOST_USER   #this for exception
        obj_selected = obj[0]
        EmailThread(obj_selected.subject, mark_safe(obj_selected.message), list_email_user).start()
    submit_email_matlab.short_description = 'Submit BroadCast DWSIM'
    submit_email_matlab.allow_tags = True

    actions = [ 'submit_email', 'submit_email_allevents', 'submit_email_ansys', 'submit_email_python', 'submit_email_scilab', 'submit_email_matlab', 'submit_email_aspen', 'submit_email_dwsim']

    list_display = ("subject", "created")
    search_fields = ['subject',]

admin.site.register(BroadCast_Email, BroadCast_Email_Admin)