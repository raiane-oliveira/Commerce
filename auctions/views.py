import locale

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
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

    # listings.delete()
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

            user = User.objects.get(id=request.user.id)
            category_id = None

            if category:
                categories = list(Categories.objects.all().values_list("category", flat=True))

                # Add new category
                if category not in categories:
                    newCategory = Categories(category=category)
                    newCategory.save()
                    category_id = newCategory
                
                # Takes a existing category
                else:
                    category_id = Categories.objects.get(category=category)


            # Add data to the auction Listing model
            newListing = AuctionListing(
                title=title, 
                description=description, 
                bid=startBid,
                imageURL=imageURL,
                category=category_id,
                user=user,
            )
            newListing.save()

            # Add bid to the Bids model
            bid = Bids(bid=startBid, listing=newListing, user=user)
            bid.save()

            return HttpResponseRedirect(reverse("index"))

        # Re-render the page with error messages
        else:
            return render(request, "auctions/createListing.html", {
                "form": form
            })

    return render(request, "auctions/createListing.html", {
        "form": FormNewListing()
    })


@login_required(login_url='login')
def listings(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)
    category = Categories.objects.get(category=listing.category)
    winner = ""
    comments = listing.comments.all()
    
    # If the user owns the listing, he can close the auction
    listingOwner = True if listing.user.id == request.user.id else False

    if request.method == 'POST':

        # Checks if the new bid is valid
        newBid = isNumber(locale.atof(request.POST["bid"]))
        if not newBid:
            return HttpResponse("Invalid Bid!")

        # Converts bid to US dollar format and take the highest bid
        newBid = locale.atof(request.POST["bid"])
        maxBid = listing.bids.aggregate(Max('bid'))

        # Checks if the new bid is higher than the other
        if newBid > maxBid['bid__max']:
            listing.bid = newBid
            listing.save()

            user = User.objects.get(pk=request.user.id)
            bids = Bids(bid=newBid, listing=listing, user=user)
            bids.save()
        else:
            return HttpResponse("Bid cannot be lower or equal than any other made!")

    # Gets winner of auction
    if listing.active == False:
        maxBid = listing.bids.aggregate(Max('bid'))
        winner = listing.bids.get(bid=maxBid["bid__max"])

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "listingOwner": listingOwner,
        "winner": winner,
        "formComments": FormComments(),
        "comments": comments
    })


@login_required(login_url='login')
def closeAuction(request, listing_id):
    if request.method == 'POST':

        # Gets listing and disable it
        listing = AuctionListing.objects.get(id=listing_id)
        listing.active = False
        listing.save()

        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))
    else:
        return HttpResponseRedirect(reverse("index"))


@login_required(login_url='login')
def watchlist(request):
    if request.method == "POST":

        # Gets data from add form
        listing_id = request.POST["listing_id"]
        choiceUser = request.POST["watchlist"]

        listing = AuctionListing.objects.get(id=listing_id)
        if choiceUser == "add":
            listing.watchlist = True
            listing.save()
        else:
            listing.watchlist = False
            listing.save()

        return HttpResponseRedirect(reverse("listings", args=(listing_id,)))

    else:
        listings = AuctionListing.objects.filter(watchlist=True).all()
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
    listings = list(AuctionListing.objects.filter(category=category_id.id).all())

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
            newComment = Comments(comment=commentText, user=user, listing=listing)
            newComment.save()

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