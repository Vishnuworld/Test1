from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import fields

from .models import CustomUser, ProductInCart


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

from django import forms
from django.core.validators import RegexValidator
from firstapp.models import Contact

class ContactUsForm(forms.ModelForm):
    # name = forms.CharField(max_length=100, required=True)
    # email = forms.EmailField(required=True)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = forms.CharField(validators=[phone_regex], max_length=17)
    # query = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Contact
        fields = '__all__'
        