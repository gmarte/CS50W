from cProfile import label
from click import style
from django import forms
from django.shortcuts import render


from . import util


class NewEntry(forms.Form):
    title = forms.CharField(label="Title:")
    content = forms.CharField(label="Markdown Content:", widget=forms.Textarea)
    # content = forms.Textarea(label="Markdown Content:")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "entry": util.get_entry(entry)
    })


def add(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        if form.is_valid():
            util.save_entry(
                form.cleaned_data["title"], form.cleaned_data["content"])
            return render(request, "encyclopedia/entry.html", {
                "title": form.cleaned_data["title"],
                "entry": util.get_entry(form.cleaned_data["title"])
            })
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": NewEntry()
        })
