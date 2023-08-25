from django import forms
from .models import NewsModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=150)
    news_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = NewsModel
        fields = ["title", "news_content"]



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
