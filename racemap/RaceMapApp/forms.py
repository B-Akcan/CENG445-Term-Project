from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "first_name", "last_name"]

class MapCreateForm(forms.Form):
    num_cols = forms.IntegerField(min_value=3, max_value=20)
    num_rows = forms.IntegerField(min_value=3, max_value=20)
    cellsize = forms.IntegerField(min_value=10, max_value=1000)
    bg_color = forms.CharField()

class ComponentCreateForm(forms.Form):
    comp_type = forms.CharField(max_length=20)
    x = forms.IntegerField(min_value=0)
    y = forms.IntegerField(min_value=0)

class ComponentRotateDeleteForm(forms.Form):
    x = forms.IntegerField(min_value=0)
    y = forms.IntegerField(min_value=0)