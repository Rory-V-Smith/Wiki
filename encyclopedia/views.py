from json.encoder import py_encode_basestring
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.urls import reverse
import markdown
from random import randint

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })  

def wiki_entry(request, title):
    html_content = convert_md_to_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def search(request):
    if request.method == 'GET':
        entry_search = request.GET['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "entry": entry_search,
                "content": html_content
            })
        else:
            all_entries = util.list_entries()
            search_results = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    search_results.append(entry)
            return render(request, "encyclopedia/search.html", {
                "search_results": search_results
            })

def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']       
        title_exists = util.get_entry(title)
        if title_exists is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            html_content = convert_md_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": html_content
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def save_edit(request):
    if request.method == "POST":
        title =  request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = convert_md_to_html(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

def random(request):
    entries = util.list_entries()
    i = randint(1, len(entries) - 1)
    random_entry = entries[i]
    return wiki_entry(request, random_entry)
    

