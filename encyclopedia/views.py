from cProfile import label
from html import entities
from random import randrange
from click import style
from django import forms
from django.shortcuts import render

from . import util


class NewEntry(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Please insert the title', 'class': 'form-control'}))
    content = forms.CharField(label="Markdown Content:", widget=forms.Textarea(
        attrs={'placeholder': 'Please insert the markdown content', 'class': 'form-control'}))
    # content = forms.Textarea(label="Markdown Content:")
    state = forms.CharField(widget=forms.HiddenInput(), initial='new')


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": util.get_entry(entry)
    })


def random(request):
    entries = util.list_entries()
    entry = entries[randrange(0, len(entries)-1)]
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": util.get_entry(entry)})


def search(request):
    if request.method == "POST":
        query = request.POST['q']  # query for the search
        entries = util.search_entry(query)
        if len(entries) > 1:
            return render(request, "encyclopedia/search.html",
                          {'query': query,
                           "entries": entries})
        elif len(entries) == 1 and entries[0] == query:
            return render(request, "encyclopedia/entry.html", {
                "title": entries[0],
                "entry": util.get_entry(entries[0])})
        elif len(entries) == 1 and query in entries[0]:
            return render(request, "encyclopedia/search.html",
                          {'query': query,
                           "entries": entries})
        else:
            return render(request, "encyclopedia/search.html", {})

    else:
        return render(request, "encyclopedia/search.html", {})


def add(request, title=None):
    if title:
        data = {'title': title, 'content': util.get_entry(
            title), 'state': 'edit'}
        form = NewEntry(data)
        return render(request, "encyclopedia/add.html", {
            "form": form
        })
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            print(form.cleaned_data["state"])
            msg = util.save_entry(
                form.cleaned_data["title"], form.cleaned_data["content"], form.cleaned_data["state"])
            if msg == "success" or msg == "edited":
                return render(request, "encyclopedia/entry.html", {
                    "title": form.cleaned_data["title"],
                    "entry": util.get_entry(form.cleaned_data["title"])
                })
            else:
                form.add_error("title", msg)
                return render(request, "encyclopedia/add.html", {
                    "form": form
                })
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewEntry()
        })
