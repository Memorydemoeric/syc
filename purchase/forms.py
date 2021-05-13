from django import forms
from purchase.models import Purchase

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['pur_handle', 'cust_id', 'pur_modify_date']