from django import forms
from .models import NewsModel


class NewsForm(forms.ModelForm):
    title = forms.CharField(max_length=150)
    news_content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = NewsModel
        fields = ["title", "news_content"]
