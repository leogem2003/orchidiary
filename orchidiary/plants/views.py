import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

from .models import OrchidInstance, OrchidVariety, OrchidGenre
from .forms import AddOrchidInstanceForm, AddOrchidGenreForm, AddVarietyForm, FilteredSearchForm

@login_required
def account_stats(request):
    user = request.user
    orchids = OrchidInstance.objects.filter(user__exact=user)
    number_of_orchids = orchids.count()
    varieties = OrchidVariety.objects.filter(pk__in=orchids.values_list('variety'))
    number_of_varieties = varieties.count()
    number_of_genres = OrchidGenre.objects.filter(pk__in=varieties.values_list('genre')).count()
    context = {
        'num_orchids':number_of_orchids,
        'num_vars': number_of_varieties,
        'num_gen': number_of_genres,
    }
    return render(request, "account/account.html", context=context)


def list_context(title, redir, add_url, page_obj, missing, my=False):
    return {
        'title':title,
        'redir':redir,
        'add_url':add_url,
        'my':my,
        'page_obj':page_obj,
        'missing':missing,
    }

@login_required
def orchids_list(request, page:int, num:int, variety=None):
    user = request.user
    orchids = OrchidInstance.objects.filter(user__exact=user).order_by("variety")
    if variety:
        orchids = orchids.filter(variety__exact=variety)
    page_obj = Paginator(orchids, num, allow_empty_first_page=True)
    missing = False if orchids.count() else True
    context = list_context("orchids", "orchids_list", "add_orchid_instance", page_obj.get_page(page), missing)
    return render(request, "list_template.html", context=context)

@login_required
def add_orchid_view(request):
    done = None
    if request.method == "POST":
        new_instance = OrchidInstance(user=request.user)
        form = AddOrchidInstanceForm(request.POST, instance=new_instance)
        if form.is_valid():
            form.save(commit=True)
            done = True
        else:
            done = False
    else:
        form = AddOrchidInstanceForm()
    context = {
        'done':done, 
        'form':form,
        'title':'orchid',
        'operation':'Add',
    }
    return render(request, "account/add_edit.html", context=context)

@login_required
def orchid_detail_view(request, pk:int):
    orchid = OrchidInstance.objects.get(pk=pk)
    return render(request, "account/instance_detail.html", context={"orchid":orchid})


def genre_list_view(request, page:int, num:int):
    genres = OrchidGenre.objects.all().order_by('genre')
    
    #context = paged_view(genres, page, num, "genre")
    page_obj = Paginator(genres, num, allow_empty_first_page=True)
    missing = False if genres.count() else True
    context = list_context("genres", "genres_list", "add_genre", page_obj.get_page(page), missing)
    return render(request, "list_template.html", context=context)


@login_required
def my_genre_list_view(request, page:int, num:int):
    user = request.user
    genres = OrchidGenre.objects.filter(genre__in = OrchidVariety.objects.filter(
            pk__in = OrchidInstance.objects.filter(user__exact=user).values_list('variety', flat=True)
        ).values_list('genre', flat=True)
    ).order_by('genre')
    
    #context = paged_view(genres, page, num)
    page_obj = Paginator(genres, num, allow_empty_first_page=True)
    missing = False if genres.count() else True
    context = list_context("genres", "genres_list", "add_genre", page_obj.get_page(page), missing, my=True)
    return render(request, "list_template.html", context=context)

def genre_detail_view(request, pk:str):
    genre = OrchidGenre.objects.get(genre=pk)
    return render(request, "genre_detail.html", context={"genre":genre})


@login_required
def add_genre_view(request):
    done = None
    if request.method == "POST":
        form = AddOrchidGenreForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            done = True
        else:
            done = False
    else:
        form = AddOrchidGenreForm()
    context = {
        'done':done, 
        'form':form,
        'title':'genre',
        'operation':'Add',
    }
    return render(request, "account/add_edit.html", context=context)

def variety_list_view(request, page:int, num:int, genre=None):
    if genre:
        varieties = OrchidVariety.objects.filter(genre__exact=genre).order_by('name')
    else:
        varieties = OrchidVariety.objects.all().order_by('genre').order_by('name')
    
    page_obj = Paginator(varieties, num, allow_empty_first_page=True)
    missing = False if varieties.count() else True
    context = list_context("genres", "genres_list", "add_genre", page_obj.get_page(page), missing, my=True)
    return render(request, "list_template.html", context=context)


@login_required
def my_variety_list_view(request, page:int, num:int, genre=None):
    user = request.user
    if genre:
        varieties = OrchidVariety.objects.filter(
            pk__in = OrchidInstance.objects.filter(user__exact=user).values_list('variety', flat=True),
            genre__exact=genre
        ).order_by("genre").order_by("name")
    else:
        varieties = OrchidVariety.objects.filter(
                pk__in = OrchidInstance.objects.filter(user__exact=user).values_list('variety', flat=True)
            ).order_by("genre").order_by("name")
    
    page_obj = Paginator(varieties, num, allow_empty_first_page=True)
    missing = False if varieties.count() else True
    context = list_context("varieties", "variety_list", "add_variety", page_obj.get_page(page), missing, my=True)
    return render(request, "list_template.html", context=context)

def variety_detail_view(request, pk:str):
    variety = OrchidVariety.objects.get(pk=pk)
    return render(request, "variety_detail.html", context={"variety":variety})

@login_required
def add_variety_view(request):
    done = None
    if request.method == "POST":
        form = AddVarietyForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            done = True
        else:
            done = False
    else:
        form = AddVarietyForm()
    context = {
            'done':done, 
            'form':form,
            'title':'variety',
            'operation':'add',
    }
    return render(request, "account/add_edit.html", context=context)

from django.forms.models import model_to_dict

def edit_gen_view(request, model, form, pk):
    done = None
    instance = model.objects.get(pk=pk)
    if request.method == "POST":
        form = form(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = model.objects.get(pk=pk)
            if(instance.image):
                print("genre", instance, "image",instance.image.path)
                try:
                    os.remove(instance.image.path)
                except FileNotFoundError: pass
            form.save(commit=True)
            done = True
        else:
            done = False
    else:
        form = form(initial=model_to_dict(instance))
    context = {
        'done':done, 
        'form':form,
    }
    return context
    
@login_required
def edit_instance_view(request, pk:int): 
    context = {
        **edit_gen_view(request, OrchidInstance, AddOrchidInstanceForm, pk),
        'title':'orchid',
        'operation':'edit',
    }
    return render(request, "account/add_edit.html", context=context)


@login_required
def edit_genre_view(request, pk:str):
    context = {
        **edit_gen_view(request, OrchidGenre, AddOrchidGenreForm, pk),
        'title':'genre',
        'operation':'edit',
    }
    return render(request, "account/add_edit.html", context=context)


@login_required
def edit_variety_view(request, pk:str):
    context = {
        **edit_gen_view(request, OrchidVariety, AddVarietyForm, pk),
        'title':'variety',
        'operation':'edit',
    }
    return render(request, "account/add_edit.html", context=context)

def delete_gen_view(request, model, pk, redirect, args):
    instance = model.objects.get(pk=pk)
    instance.delete()
    return HttpResponseRedirect(reverse(redirect, args=args))

@login_required
def delete_genre_view(request, pk:str):
    return delete_gen_view(request, OrchidGenre, pk, 'my_genres_list', (1,10))

@login_required
def delete_variety_view(request, pk:int):
    return delete_gen_view(request, OrchidVariety, pk, 'my_variety_list', (1,10))

@login_required
def delete_instance_view(request, pk:int):
    return delete_gen_view(request, OrchidInstance, pk, 'orchids_list', (1,10))

def filtered_search(request):
    varieties = []
    if request.POST:
        form = FilteredSearchForm(request.POST)
        if form.is_valid():
            print("valid")
            varieties = OrchidVariety.objects.all()
            if form.cleaned_data["genre"]:
                varieties = varieties.filter(genre=form.cleaned_data["genre"])
            if form.cleaned_data["light"]:
                varieties = varieties.filter(light__in=form.cleaned_data["light"])
            if form.cleaned_data["humidity"]:
                query = {"humidity__"+form.cleaned_data["humidity_compare"]:form.cleaned_data["humidity"]}
                varieties = varieties.filter(**query)
            if form.cleaned_data["ground"]:
                varieties = varieties.filter(ground__in=form.cleaned_data["ground"])
            if form.cleaned_data["bloom"]:
                print(form.cleaned_data["bloom"])
                varieties = varieties.filter(bloom__in=form.cleaned_data["bloom"])   
        else:
            print(form.errors.as_text())
    else:
        form = FilteredSearchForm()
    
    context = {
        'form':form,
        'results':varieties
    }

    return render(request, "research.html", context=context)