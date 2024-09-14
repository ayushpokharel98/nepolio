from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from datetime import date
from .tools import return_js_names
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label="First Name:")
    last_name = forms.CharField(max_length=30, label="Last Name:")
    email = forms.EmailField(max_length=254, label="Email:")
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({
            "class": "w-full"
        })
        self.fields["last_name"].widget.attrs.update({
            "class": "w-full"
        })
        self.fields["email"].widget.attrs.update({
            "class": "w-full"
        })
        self.fields["username"].widget.attrs.update({
            "class": "w-full",
        })
        self.fields["password1"].widget.attrs.update({
            "class": "w-full"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "w-full"
        })
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2' ]

class LoginForm(AuthenticationForm):
    def __init__(self, request: Any = ..., *args: Any, **kwargs: Any) -> None:
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "w-full"
        })
        self.fields["password"].widget.attrs.update({
            "class": "w-full"
        })

class AddStockForm(forms.Form):
    stock = forms.CharField(label="Stock:", widget=forms.Select(attrs={'id': 'stock-select'}))
    quantity = forms.IntegerField(label="Quantity:")
    at_bought = forms.FloatField(label="Purchase Price:")
    date_bought = forms.DateField(label = "Date Purchased:", input_formats=['%Y-%m-%d'], initial=date.today)
    type = forms.ChoiceField(choices=[("IPO", "IPO"),("Secondary", "Secondary")], label="Type:")