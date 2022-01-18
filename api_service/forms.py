from django import forms


class SignUpIn(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=25,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    password = forms.CharField(
        label="Password",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Password"}),
    )
