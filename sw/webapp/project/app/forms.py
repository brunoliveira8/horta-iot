from registration.forms import RegistrationForm
from django import forms
from .models import Configuracao

class RegistrationForm(RegistrationForm):
    is_human = forms.BooleanField(label="Are you human?", required=False)


class ConfiguracaoForm(forms.ModelForm):
    teto = forms.IntegerField(max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': "form-control"}))
    piso = forms.IntegerField(max_value=100, min_value=0, widget=forms.NumberInput(attrs={'class': "form-control"}))
    intervalo = forms.IntegerField(max_value=20, min_value=1, widget=forms.NumberInput(attrs={'class': "form-control"}))

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Configuracao

    def clean(self):
        cleaned_data = super(ConfiguracaoForm, self).clean()
        teto = cleaned_data.get("teto")
        piso = cleaned_data.get("piso")

        if piso > teto:
            msg = "O valor do piso deve ser menor que o valor do teto."
            self.add_error('piso', msg)

