from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entrypage(request, name):
    return render(request, "encyclopedia/entrypage.html", {
        "entrytitle": name,
        "pages": util.get_entry(name)
    })


def search(request):
    results = []

    if request.method == "GET":
        check = util.list_entries()
        query = request.GET.get("q", None) #gets value from input, default None

        if query:
            for test in check:
                if query.lower() == test.lower():
                    #go to entry with same name
                    return redirect('encyclopedia:entrypage', test)
                    
                elif query.lower() in test.lower():
                    #add to list of possible matches
                    results.append(test)
        
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query
        })
    
    else:
        return render(request, "encyclopedia/search.html", {

        })
        

def new(request):
    return render(request, "encyclopedia/new.html", {
        "entries": util.list_entries()
    })


def edit(request):
    return render(request, "encyclopedia/edit.html", {
        "entries": util.list_entries()
    })


def random(request):
    #do a random number roll based on the number of data entries and pick an
    #the corresponding index 
    #redirect to entrypage
    return render(request, "encyclopedia/entrypage.html", {
        "entries": util.list_entries()
    })