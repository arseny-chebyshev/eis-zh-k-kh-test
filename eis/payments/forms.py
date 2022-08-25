from django import forms
from payments.models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['date']
    
    def clean(self):
        return super().clean()