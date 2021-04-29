from django.shortcuts import render
from django.http import HttpResponse
import markdown2
from django import forms
import re
import random

from . import util

class SearchForm(forms.Form):
    querry = forms.CharField(label='Search', max_length=10)

class NewPage(forms.Form):
    title = forms.CharField(max_length=10)
    data = forms.CharField(widget=forms.Textarea(), label='')

def edit(request, name):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            data = form.cleaned_data["data"]
            util.save_entry(name, data)
            entry = util.get_entry(name)
            md = markdown2.Markdown()
            entry = md.convert(entry)
            return render(request, "encyclopedia/page.html", {
                "entry": entry,
                "heading": name
            })
        else:
            return HttpResponse("Invalid Input")
    else:
        context = {
            "edit_form": NewPage({'title': name,
            'data': util.get_entry(name)}),
        }
        return render(request, "encyclopedia/edit.html", context)

def new_page(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/new.html", {
                    "Form": NewPage(),
                    "Message": "Entry with this name already exists"
                })
            data = form.cleaned_data["data"]
            util.save_entry(title, data)
            entry = util.get_entry(title)
            md = markdown2.Markdown()
            entry = md.convert(entry)
            return render(request, "encyclopedia/page.html", {
                "entry": entry,
                "heading": title
            })
        else:
            return HttpResponse("There was a Problem!")
    else:
        return render(request, "encyclopedia/new.html", {
            "Form": NewPage()
        })

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, name):
    if util.get_entry(name) is None:
        return HttpResponse("This entry does not exist!")
    else:
        entry = util.get_entry(name)
        md = markdown2.Markdown()
        entry = md.convert(entry)
        return render(request, "encyclopedia/page.html", {
            "entry": entry,
            "name": name
        })

def search(request):
    form = SearchForm(request.GET)
    if form.is_valid():
        querry = form.cleaned_data["querry"]
    entries = util.list_entries()
    results = []
    for entry in entries:
        if entry == querry:
            entry = util.get_entry(entry)
            md = markdown2.Markdown()
            entry = md.convert(entry)
            return render(request, "encyclopedia/page.html", {
                "entry": entry
            })
        elif re.search(querry, entry):
            results.append(entry)
    if not results:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "message": "No results found for the querry!"
        })
    else:
        return render(request, "encyclopedia/search.html", {
        "entries": results
        })

def random_page(request):
    entries = util.list_entries()
    entry = random.randint(0, len(entries) - 1)
    page = entries[entry]
    entry = util.get_entry(page)
    md = markdown2.Markdown()
    entry = md.convert(entry)
    return render(request, "encyclopedia/page.html", {
        "entry": entry,
    })
