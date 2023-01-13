from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *


def index(request):
    user = User.objects.get(pk=request.user.id)
    listings = AuctionListing.objects.all()

    # listings.delete()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "user": user,
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


def create_listing(request):
    if request.method == "POST":

        # Creates form with data
        form = FormNewListing(request.POST)

        # Checks if the form is valid
        if form.is_valid():

            # Gets data from form
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            startBid = form.cleaned_data["bid"]
            imageURL = form.cleaned_data["imageURL"]
            category = form.cleaned_data["category"]

            user = User.objects.get(pk=request.user.id)

            # Add data to the auction Listing model
            newListing = AuctionListing(
                title=title, 
                description=description, 
                imageURL = imageURL,
                bid=startBid,
                user=user,
            )
            newListing.save()

            # Add category
            newCategory = Categories(category=category, listing=newListing)
            newCategory.save()

            # Add bid to the Bids model
            bid = Bids(newBid=startBid, listing=newListing)
            bid.save()

            # newListing.active.add(newListing)

            return HttpResponseRedirect(reverse("index"))

        # Re-render the page with error messages
        else:
            return render(request, "auctions/createListing.html", {
                "form": form
            })

    return render(request, "auctions/createListing.html", {
        "form": FormNewListing()
    })
