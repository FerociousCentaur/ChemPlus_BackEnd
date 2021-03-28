from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Spectator
from django import forms
#from localflavor.in_.forms import INStateSelect, INZipCodeField, INPhoneNumberField
from .choices import college, department, program, year, gender, state

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

def validate_field(value):
    if not re.match(r'^[A-Za-z0-9_ .@-]+$', value):
        raise ValidationError(
            _('%(value)s is not an Valid Input'),
            params={'value': value},
        )


def validate_number(value):
    if not re.match(r'^[0-9]+$', value):
        raise ValidationError(
            _('%(value)s is not an Valid Input'),
            params={'value': value},
        )






class RegisterForm(forms.Form):
    f_name = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}), required=True, validators=[validate_field])
    l_name = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}), required=True, validators=[validate_field])
    gen = forms.ChoiceField(label='',
                    initial="Gender", choices=gender, required=True, widget=forms.Select(attrs={'class': "custom-select"}))

#widget=forms.TextInput(attrs={'class': "form-control"})
class RegisterForm1(forms.Form):
    email = forms.EmailField(label='',
                    widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}), required=True, validators=[validate_field])
    mob_number = forms.IntegerField(label='', max_value=999999999999999, required=True, widget=forms.NumberInput(attrs={'placeholder': '', 'class': "form-control"}))#forms.CharField(label='',
    #                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=True)
    alt_phone_number = forms.IntegerField(label='', max_value=999999999999999, required=False, widget=forms.NumberInput(attrs={'placeholder': '(Optional)', 'class': "form-control"})) #= forms.ChoiceField(label='',
                   # initial="Gender", choices=gender, required=True)
    address = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': '(Optional)', 'class': "form-control"}), validators=[validate_field])
    zipcode = forms.IntegerField(label='',max_value=9999999, required=True, widget=forms.NumberInput(attrs={'placeholder': '', 'class': "form-control"}))
    #zipcode = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Pincode', 'class': "form-control"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if Spectator.objects.filter(email=email).exists():
            raise forms.ValidationError("Looks like you have already registered!!! Click on 'Didn't Receive the Chemplus ID' to receive the ID again.")
        # elif (Spectator.objects.filter(email=email).exists()) and (not Spectator.objects.get(email=email).verified):
        #     Spectator.objects.filter(email=email).delete()
        return email
class RegisterForm2(forms.Form):
    stat = forms.ChoiceField(label='', choices=state, required=True ,widget=forms.Select(attrs={'class': "custom-select"}))
    college = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}), validators=[validate_field])#forms.CharField(label='',
    #                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=True)
    departmen = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}), validators=[validate_field])
    progra = forms.ChoiceField(label='', choices=program, required=True, widget=forms.Select(attrs={'class': "custom-select"}))
    yea = forms.ChoiceField(label='', choices=year, required=True, widget=forms.Select(attrs={'class': "custom-select"}))

class OTPVerify(forms.Form):
    email_otp = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}), validators=[validate_field])

class reaskEmail(forms.Form):
    email = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}))


class programRegister(forms.Form):
    chem_id = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}), validators=[validate_field])
    email = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}), validators=[validate_field])
    OPTIONS = (
            ("All events pass", "All events pass"),
            # ("Ansys", "Ansys"),
            # ("Python", "Python"),
            #("SciLab", "SciLab"),
            #("Matlab", "Matlab"),
            ("Aspen", "Aspen"),
            #("DWSIM", "DWSIM"),
        )
    programs = forms.MultipleChoiceField(widget=forms.SelectMultiple(attrs={'class':"selectpicker form-control",'data-selected-text-format':"count", 'OnChange':'myFunction();'}),
                                         choices=OPTIONS, required=True)
    amount = forms.CharField( disabled=True, required=False,max_length=30,widget=forms.TextInput(attrs={'placeholder': '', 'class': "form-control"}))
# class RegisterForm(forms.ModelForm):
#
#     class Meta:
#         model = Spectator
#         fields = ("first_name", "last_name", 'gender')
#         labels = {
#             'first_name': _(''),
#             'last_name': _(''),
#             'gender': _('')
#         }
#         help_texts = {
#             'first_name': _('First Name'),
#             'last_name': _('Last Name'),
#             'gender': _('Gender'),
#         }
#         error_messages = {
#             'first_name': {
#                 'max_length': _("Try using a short form of name"),
#             },
#             'last_name': {
#                 'max_length': _("Try using a short form of name"),
#             },
#         }
#
# class RegisterForm1(forms.ModelForm):
#     address = forms.CharField(required=False)
#     mob_number = INPhoneNumberField(required=True)
#     alt_mobile_number = INPhoneNumberField(required=False)
#     class Meta:
#         model = Spectator
#         fields = ("email", "mob_number", 'alt_mobile_number', 'address', 'zipcode')
#         labels = {
#             'email': _(''),
#             'mob_number': _(''),
#             'alt_mobile_number': _(''),
#             'address': _(''),
#             'zipcode': _('')
#         }
#         help_texts = {
#             'email': _('Email'),
#             'mob_number': _('Mobile number'),
#             'alt_mobile_number': _('Alt. mobile number'),
#             'address': _('Address'),
#             'zincode': _('Pincode')
#         }
#
#
# class RegisterForm2(forms.ModelForm):
#
#     class Meta:
#         model = Spectator
#         fields = ("state", "college", 'department', 'program', 'year')
#         labels = {
#             'state': _(''),
#             'college': _(''),
#             'department': _(''),
#             'program': _(''),
#             'year': _('')
#         }
#         help_texts = {
#             'state': _('State'),
#             'college': _('College'),
#             'department': _('Department'),
#             'program': _('Program'),
#             'year': _('Year')
#         }








