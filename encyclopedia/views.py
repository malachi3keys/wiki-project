from django.shortcuts import render, redirect
import random
from markdown2 import Markdown
from django import forms
from . import util

class NewPageForm(forms.Form):
    pageName = forms.CharField(label="File Name:", min_length=1, max_length=50, widget=forms.TextInput(attrs={"autofocus": True}))
    pageContent = forms.CharField(label="Page Content (markdown language):", widget=forms.Textarea)

class EditPageForm(forms.Form):
    editContent = forms.CharField(widget=forms.Textarea(attrs={"autofocus": True}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entrypage(request, name):
    #redirect pages with same spelling, but different capitilization 
    #to existing page name 
    entries = util.list_entries()
    counter = 0
    
    for check in entries:
        if name.lower() == check.lower(): 
            name = entries[counter]
        counter += 1


    pages = util.get_entry(name)

    #check that there is content for the page
    if pages:
        pages = Markdown().convert(util.get_entry(name))

    return render(request, "encyclopedia/entrypage.html", {
        "entrytitle": name,
        "pages": pages
    })


def search(request):
    results = []
    entries = util.list_entries()
    query = request.GET.get("q", None) #gets value from input, default None

    if query:
        for check in entries:
            if query.lower() == check.lower():
                #go to entry with same name
                return redirect('encyclopedia:entrypage', check)
                
            elif query.lower() in check.lower():
                #add to list of possible matches
                results.append(check)
    
    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query
    })
    

def new(request):
    duplicate = "no"

    if request.method == 'POST':
        form = NewPageForm(request.POST)

        if form.is_valid(): 
            name = form.cleaned_data["pageName"]
            entries = util.list_entries()
            
            #check if there's already a file with that name
            for check in entries:
                if name.lower() == check.lower():
                    duplicate = "Error: Already have an entry with same file name"
                
            #if new name, get contents & save file
            if duplicate == "no":
                content = form.cleaned_data["pageContent"]
                util.save_entry(name, content)
            
                return redirect('encyclopedia:entrypage', name)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewPageForm()

    return render(request, "encyclopedia/new.html", {
        "form": form,
        "duplicate": duplicate
    })


def edit(request, name):
    #button from entry page leads edit page  
    #textarea is prepopulated with the file content
    if request.method =='GET': 
        entry = util.get_entry(name)
        eform = EditPageForm(initial={"editContent": entry})

        return render(request, "encyclopedia/edit.html", {
            "form": eform,
            "name": name
        })

    #when save button pressed, save file and redirect to entry page    
    elif request.method == 'POST':
        eform = EditPageForm(request.POST)
        
        if eform.is_valid():
            entry = eform.cleaned_data["editContent"]
            util.save_entry(name, entry) 
            return redirect('encyclopedia:entrypage', name)


def random_page(request):
    #pick a random entry from list of entries and redirect to page
    entries = util.list_entries()
    name = random.choice(entries)

    return redirect('encyclopedia:entrypage', name)