from .models import OrderItem
from django import forms

class QuantityForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']