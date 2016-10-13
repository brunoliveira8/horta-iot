from registration.forms import RegistrationForm
from django import forms
 
class RegistrationForm(RegistrationForm):
    is_human = forms.BooleanField(label="Are you human?", required=False)


