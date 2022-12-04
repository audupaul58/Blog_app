from django.forms import ModelForm
from django import forms
from .models import Article

class Blog_form(ModelForm):
    
    MYCHOICE = (
        ("Hospitality", "Hospitality"),
        ("Marketing", "Marketing"),
        ("Technology", "Technology")
    )
    
    STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
    )
    
    
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'style': 'width: 300px;', 'class': 'form-control'}))
    body = forms.Textarea(attrs={'placeholder': 'Descriptions', 'style': 'width: 300px;', 'class': 'form-control'})
    image = forms.FileField()
    category = forms.ChoiceField(choices=MYCHOICE)
    status = forms.ChoiceField(choices=STATUS_CHOICES)
    tags = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Tags', 'style': 'width: 300px;', 'class': 'form-control'}))
    
    class Meta:
        model = Article
        exclude = ('slug', "author" )