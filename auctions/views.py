from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json

from .models import User, Auction, Category, Bid, Comment, Watchlist
from .forms import ListingForm


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def newlisting(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            starting_bid = form.cleaned_data['starting_bid']
            category = form.cleaned_data['category']

            listingCreated = Auction.objects.create(
                user=request.user,
                title=title,
                description=description,
                image=image,
                starting_bid=starting_bid,
                category=category
            )
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/newlisting.html", {
            'form': ListingForm()
        })

def addCategory(request):
    data = json.loads(request.body)
    newcategory = data["newCategory"]
    newcategory= newcategory.capitalize()
    try:
        categoryAdded = Category.objects.create(category = newcategory)
        categoryAdded.save()
    except IntegrityError:
        return JsonResponse({"str":""})
    return JsonResponse({"str":"success"})
