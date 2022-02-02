from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
import os
import random

from .models import User, Auction, Category, Bid, Comment, Watchlist
from .forms import ListingForm


def index(request):
    auctions = Auction.objects.all().order_by('id').reverse()
    categories = Category.objects.all().order_by('category')
    if request.user.is_authenticated:
        watchlist= Watchlist.objects.get(user=request.user)
        watchlistno = watchlist.auction.count()
    else:
        watchlistno = '0'
    DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(DIR, "./media/images")
    imgList= os.listdir(path) 
    random.shuffle(imgList)
    first = imgList[0]
    imgList.pop(0)
    return render(request, "auctions/index.html", {
        'auctions': auctions,
        'categories': categories,
        'watchlistno': watchlistno,
        'images': imgList,
        'first': first
    })


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
        watchlist = Watchlist.objects.create(user= user)
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'auctions/register.html')


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
        watchlist= Watchlist.objects.get(user=request.user)
        watchlistno = watchlist.auction.count()
        return render(request, "auctions/newlisting.html", {
            'form': ListingForm(),
            'watchlistno': watchlistno
        })

def addCategory(request):
    if request.method == "POST":
        data = json.loads(request.body)
        newcategory = data["newCategory"]
        if newcategory == "":
            return JsonResponse({"str":""})
        newcategory= newcategory.capitalize()
        try:
            categoryAdded = Category.objects.create(category = newcategory)
            categoryAdded.save()
        except IntegrityError:
            return JsonResponse({"str":""})
        return JsonResponse({"str":"success"})

def viewCategory(request, category):
    categories = Category.objects.exclude(category= category).all().order_by('category')
    categoryid = Category.objects.get(category= category)
    auctions= Auction.objects.filter(category= categoryid).order_by('id').reverse()
    if request.user.is_authenticated:
        watchlist= Watchlist.objects.get(user=request.user)
        watchlistno = watchlist.auction.count()
    else:
        watchlistno = '0'
    return render(request, 'auctions/viewCategory.html', {
        'category': category,
        'categories': categories,
        'auctions': auctions,
        'watchlistno': watchlistno
    })

@login_required(login_url='/login')
def viewAuction(request, auctionId):
    watchlist= Watchlist.objects.get(user= request.user)
    auction = Auction.objects.get(id= auctionId)
    comments = auction.comments.all().order_by('id').reverse()
    watchlist= Watchlist.objects.get(user=request.user)
    watchlistno = watchlist.auction.count()
    return render(request, 'auctions/viewAuction.html', {
        'auction': auction,
        'watchlist': watchlist,
        'comments': comments,
        'auctionId': auctionId,
        'watchlistno': watchlistno
    })

def deleteListing(request, auctionId):
    auction = Auction.objects.get(id = auctionId)
    if auction.user == request.user:
        auction.delete()
        return HttpResponseRedirect(reverse("index"))

def addComment(request, auctionId):
    if request.method == "POST":
        auction =Auction.objects.get(id= auctionId)
        newComment = request.POST["commentbyuser"]
        newCommentCreated = Comment.objects.create(comment=newComment, user= request.user)
        auction.comments.add(newCommentCreated)
        auction.save()
        return HttpResponseRedirect(reverse("viewAuction", args=(auctionId,)))

def deleteComment(request, commentId):
    if request.method == 'GET':
        comment = Comment.objects.get(id = commentId)
        comment.delete()
        return JsonResponse({'status':'success'})

def placeBid(request):
    if request.method == "POST":
        data = json.loads(request.body)
        auctionId = data["auctionId"]
        bid = data["bid"]
        auction = Auction.objects.get(id = int(auctionId))
        newBid = Bid.objects.create(user= request.user, auction= auction, bid= float(bid))
        auction.latest_bid= newBid
        auction.save()
        return JsonResponse({'status':'success'})

def closeLisitng(request, auctionId):
    if request.method == 'GET':
        auction = Auction.objects.get(id = auctionId)
        auction.close = True
        auction.save()
        return JsonResponse({'status':'success'})

@login_required(login_url='/login')
def myListing(request):
    user = request.user
    watchlist= Watchlist.objects.get(user=request.user)
    watchlistno = watchlist.auction.count()
    return render(request, 'auctions/myListing.html', {
        "auctions": user.user_action_listing.all().order_by('id').reverse(),
        'watchlistno': watchlistno
    })

def addremoveWatchlist(request, auctionId):
    if request.method == 'GET':
        auction = Auction.objects.get(id = auctionId)
        user= request.user
        watchlist= Watchlist.objects.get(user=user)
        if auction in watchlist.auction.all():
            watchlist.auction.remove(auction)
            watchlist.save()
        else:
            watchlist.auction.add(auction)
            watchlist.save()
        watchlistno = watchlist.auction.count()
        return JsonResponse({'status':watchlistno})

@login_required(login_url='/login')
def viewWatchlist(request):
    user= request.user
    watchlist= Watchlist.objects.get(user= request.user)
    watchlistno= watchlist.auction.count()
    auctions= watchlist.auction.all().order_by('id').reverse()
    return render(request, 'auctions/viewWatchlist.html', {
        'watchlistno': watchlistno,
        'auctions': auctions
    })


