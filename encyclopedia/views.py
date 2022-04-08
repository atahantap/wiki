from django.shortcuts import render
import markdown2
from . import util
from django import forms
import random
from django.http import HttpResponse

class newPageForm(forms.Form):
    title = forms.CharField(label="Title",
        widget=forms.Textarea(attrs={
        'style': 'width:200%; height:30px'
        }))
    content = forms.CharField(label="Content",
        widget=forms.Textarea(attrs={
        'style': 'width:300%; height: 150px'
        }))

class editPageForm(forms.Form):
    content = forms.CharField(label="Content",
        widget=forms.Textarea(attrs={
        'style': 'width:300%; height: 150px'
        }))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    md = markdown2.Markdown()
    if request.method == 'GET':
        if entry_name in util.list_entries():
            return render(request, "encyclopedia/entry.html", {
                "title": entry_name,
                "content": md.convert(util.get_entry(f"{entry_name}"))
            })
        else:
            return render(request, "encyclopedia/errorpage.html")    

    elif request.method == 'POST':
        form = editPageForm(request.POST)
        if form.is_valid():
            title = entry_name
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": md.convert(util.get_entry(f"{title}"))
                })
        else:
            return HttpResponse("form not valid")


def newpage(request):
    if request.method == 'POST':
        form = newPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/existingentry.html", {
                    "title": title
                })
            else:
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                md = markdown2.Markdown()
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "content": md.convert(util.get_entry(f"{title}"))
                })

    else:
        return render(request, "encyclopedia/newpage.html", {
        "newPageForm": newPageForm(),
        })


def randompage(request):
    list = util.list_entries()
    n = len(list)
    r = random.randint(0,n-1)
    title = list[r]
    md = markdown2.Markdown()
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": md.convert(util.get_entry(f"{title}"))
    })

def editpage(request, title):
    if request.method == 'GET':
        content = util.get_entry(f"{title}")
        return render(request, "encyclopedia/editpage.html", {
            "title": title,
            "content": content,
            "editPageForm": editPageForm(initial={"content": f"{content}"})
        })

def search(request):
    if request.method == 'GET':
        searched = request.GET['q']
        entry_list = util.list_entries()
        if searched in entry_list:
            md = markdown2.Markdown()
            return render(request, "encyclopedia/entry.html", {
                "title": searched,
                "content": md.convert(util.get_entry(f"{searched}"))
            })
        else:
            search_results = []
            for entry in entry_list:
                if searched in entry:
                    search_results.append(entry)
            success_flag = len(search_results)
            #acts like a boolean to determine if there were any search results
            return render(request, "encyclopedia/searchresults.html", {
                "success": success_flag,
                "searched": searched,
                "results": search_results
            })
