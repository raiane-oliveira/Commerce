import locale

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import *
from .forms import *

# Configure locale library to format numbers in USD money format
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def index(request):
    listings = AuctionListing.objects.filter(active=True).all()
    return render(request, "auctions/index.html", {
        "listings": listings,
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
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='login')
def create_listing(request):
    if request.method == "POST":

        # Creates form with data
        form = FormNewListing(request.POST)

        # Checks if the form is valid
        if form.is_valid():

            # Gets data from form
            title = form.cleaned_data["title"].strip()
            description = form.cleaned_data["description"]
            startBid = form.cleaned_data["bid"]
            imageURL = form.cleaned_data["imageURL"]
            category = form.cleaned_data["category"].strip().capitalize()

            if category:
                categories = list(Categories.objects.all().values_list("category", flat=True))

                if category not in categories:
                    category = Categories.objects.create(category=category)
                else:
                    category = Categories.objects.get(category=category)
            else:
                category = None

            # Add data to the auction Listing model
            user = User.objects.get(id=request.user.id)
            newListing = AuctionListing.objects.create(
                title=title, 
                description=description, 
                bid=startBid,
                imageURL=imageURL,
                category=category,
                user=user,
            )

            # Adds starting bid to track all other bids
            bid = Bids.objects.create(bid=startBid, listing=newListing, user=user)

            watchlist = Watchlist.objects.create(listing=newListing, user=user)

            return HttpResponseRedirect(reverse("index"))

        # Re-render the page with error messages
        else:
            return render(request, "auctions/createListing.html", {
                "form": form,
            })

    return render(request, "auctions/createListing.html", {
        "form": FormNewListing()
    })


@login_required(login_url='login')
def listings(request, listing_id):

    # Gets listing by its id and all its comments
    listing = AuctionListing.objects.get(id=listing_id)
    comments = listing.comments.all()

    # Checks if there is a watchlist for the listing, otherwise creates one
    try:
        watchlist = Watchlist.objects.get(listing=listing, user=request.user.id)
    except:
        user = User.objects.get(id=request.user.id)
        watchlist = Watchlist.objects.create(listing=listing, user=user)

    winner = None

    # Highest bidder
    maxBid = listing.bids.aggregate(Max('bid'))

    # Gets amount of bids and current bid of user
    amountBids = listing.bids.count()
    currentBidUser = listing.bids.get(bid=maxBid["bid__max"]).user

    # Gets winner of auction
    if listing.active == False:
        winner = listing.bids.get(bid=maxBid["bid__max"])

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "winner": winner,
        "watchlist": watchlist,
        "comments": comments,
        "formComments": FormComments(),
        "formNewBid": FormNewBid(),
        "amountBids": amountBids,
        "currentBidUser": currentBidUser
    })


@login_required(login_url='login')
def newBid(request, listing_id):
    if request.method == 'POST':
        form = FormNewBid(request.POST)

        if form.is_valid():

            # Gets listing by id
            listing = AuctionListing.objects.get(id=listing_id)

            # Takes the new bid and the highest bid from listing
            newBid = form.cleaned_data["bid"]
            maxBid = listing.bids.aggregate(Max('bid'))

            # Checks if the new bid is higher than the other
            if newBid > maxBid['bid__max']:
                listing.bid = newBid
                listing.save()

                user = User.objects.get(pk=request.user.id)
                bids = Bids.objects.create(bid=newBid, listing=listing, user=user)
            else:
                return render(request, "auctions/error.html", {
                    "message": "Bid cannot be lower or equal than any other made"
                })

            return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
        else:
            return render(request, "auctions/error.html", {
                "message": "Invalid Bid"
            })

    return HttpResponseRedirect(reverse("index"))


@login_required(login_url='login')
def closeAuction(request, listing_id):

    # Gets listing and disable it
    if request.method == 'POST':
        listing = AuctionListing.objects.filter(id=listing_id).update(active=False)
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url='login')
def watchlist(request):
    user = User.objects.get(id=request.user.id)
    if request.method == "POST":

        # Gets data from form
        listing_id = request.POST["listing_id"]
        choiceUser = request.POST["watchlist"]

        listing = AuctionListing.objects.get(id=listing_id)

        if choiceUser == "add":
            Watchlist.objects.filter(listing=listing, user=user).update(watchlist=True)
        else:
            Watchlist.objects.filter(listing=listing, user=user).update(watchlist=False)
            
        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))

    # listings = Watchlist.objects.filter(watchlist=True, user=request.user.id).all()
    listings = user.userWatchlist.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })


@login_required(login_url='login')
def categories(request):
    categories = Categories.objects.all()
    return render(request, 'auctions/categories.html', {
        "categories": categories,
    })


@login_required(login_url="login")
def categoryPage(request, category):

    # Gets all active listings in that category
    category_id = Categories.objects.get(category=category)
    listings = list(AuctionListing.objects.filter(category=category_id.id, active=True).all())

    return render(request, "auctions/categoryPage.html", {
        "listings": listings,
        "category": category
    })


@login_required(login_url="login")
def comments(request, listing_id):
    if request.method == "POST":
        form = FormComments(request.POST)

        if form.is_valid():

            # Gets data
            commentText = form.cleaned_data["comment"].strip()
            user = User.objects.get(id=request.user.id)
            listing = AuctionListing.objects.get(id=listing_id)

            # Add comment to model django
            newComment = Comments.objects.create(comment=commentText, user=user, listing=listing)
            return HttpResponseRedirect(reverse("listings", args=(listing_id,)))

        else:
            return render(request, "auctions/listing.html", {
                "formComments": form
            })

    else:
        return HttpResponseRedirect(reverse("index"))



def isNumber(value):
    try:
        float(value)
    except ValueError:
        return False
    return True