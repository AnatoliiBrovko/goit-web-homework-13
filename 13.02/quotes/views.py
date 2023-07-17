from django.shortcuts import render, redirect

from django.core.paginator import Paginator
from .utils import get_mongodb
from .form import TagForm, AuthorForm, QuoteForm
from .models import Author, Quote
from pymongo import MongoClient

# Create your views here.


def main(request, page=1):

    db = get_mongodb()
    quotes = db.quotes.find()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={"quotes":quotes_on_page})


def get_mongodb():
    client = MongoClient('mongodb://localhost')
    db = client.hw
    return db    


def author(request, _id):

    author = Author.objects.get(pk=_id)
    return render(request, "quotes/author.html", context={'author': author})


def new_author(request):

    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='quotes:root')
        else:
            return render(request, 'quotes/new_author.html', context={'form': AuthorForm(), 'message': 'Form not valid'})
    return render(request, 'quotes/new_author.html', context={'form': AuthorForm()})


def new_quote(request):

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:root")
        else:
            return render(request, "quotes/new_quote.html", context={'form': QuoteForm(), "message": "Form not valid"})
    return render(request, "quotes/new_quote.html", context={'form': QuoteForm()})


def new_tag(request):
    
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes:root")
        else:
            return render(request, "quotes/new_tag.html", context={'form': TagForm(), "message": "Form not valid"})
    return render(request, "quotes/new_tag.html", context={'form': TagForm()})
