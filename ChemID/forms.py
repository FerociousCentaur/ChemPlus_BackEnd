from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import Spectator
from django import forms
#from localflavor.in_.forms import INStateSelect, INZipCodeField, INPhoneNumberField
from .choices import college, department, program, year, gender, state

class RegisterForm(forms.Form):
    f_name = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=True)
    l_name = forms.CharField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Last Name'}), required=True)
    gen = forms.ChoiceField(label='',
                    initial="Gender", choices=gender, required=True)


class RegisterForm1(forms.Form):
    email = forms.EmailField(label='',
                    widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
    mob_number = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Ph. Number'}))#forms.CharField(label='',
    #                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=True)
    alt_phone_number = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Alt. Ph. Number'})) #= forms.ChoiceField(label='',
                   # initial="Gender", choices=gender, required=True)
    address = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'placeholder': 'Address'}))
    zipcode = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Pincode'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if Spectator.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists!!! Click on \n'Didn't Receive the Chemplus ID'\n to receive the ID again.")
        # elif (Spectator.objects.filter(email=email).exists()) and (not Spectator.objects.get(email=email).verified):
        #     Spectator.objects.filter(email=email).delete()
        return email
class RegisterForm2(forms.Form):
    stat = forms.ChoiceField(label='', choices=state, required=True)
    college = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'College'}))#forms.CharField(label='',
    #                 widget=forms.TextInput(attrs={'placeholder': 'First Name'}), required=True)
    departmen = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Department'}))
    progra = forms.ChoiceField(label='', choices=program, required=True)
    yea = forms.ChoiceField(label='', choices=year, required=True)

class OTPVerify(forms.Form):
    email_otp = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Email OTP'}))

class reaskEmail(forms.Form):
    email = forms.EmailField(label='', required=True, widget=forms.TextInput(attrs={'placeholder': 'Email ID'}))

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








