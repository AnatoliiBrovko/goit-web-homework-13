from django.forms import ModelForm, CharField, TextInput, ModelChoiceField
from .models import Tag, Author, Quote


class TagForm(ModelForm):

    name = CharField(max_length=50, required=True, widget=TextInput())
    
    class Meta:
        model = Tag
        fields = ['name']

class AuthorForm(ModelForm):
    
    fullname = CharField(max_length=25, required=True, widget=TextInput())
    born_date = CharField(max_length=25, required=True, widget=TextInput())
    born_location = CharField(max_length=100, required=True, widget=TextInput())
    description = CharField(widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

class QuoteForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all())
    quote = CharField(max_length=5000, required=True, widget=TextInput)

    class Meta:
        model = Quote
        fields = ['author', 'quote']
        exclude = ['tags']