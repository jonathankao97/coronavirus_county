from django import forms
from django.core.validators import RegexValidator

EMAIL_FIELD_VALIDATOR = RegexValidator(r'^\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b$', message="Invalid Email Format")

class EmailSignUp(forms.Form):
    email = forms.CharField(max_length=100, validators=[EMAIL_FIELD_VALIDATOR], label="Email")


