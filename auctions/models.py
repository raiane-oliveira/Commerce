from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class User(AbstractUser):
    pass


class Categories(models.Model):
    category = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.category}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    bid = models.DecimalField(max_digits=100, decimal_places=2)
    imageURL = models.URLField(blank=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="categories", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userListing")

    active = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.description} | {self.bid}"

    class Meta:
        ordering = [F("id").desc()]


class Watchlist(models.Model):
    watchlist = models.BooleanField(default=False)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userWatchlist")

    def __str__(self):
        return f"{self.user}: {self.listing.title} - {self.watchlist}"


class Bids(models.Model):
    bid = models.DecimalField(max_digits=100, decimal_places=2)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBids")

    def __str__(self):
        return f"{self.bid}"


class Comments(models.Model):
    comment = models.TextField(blank=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.comment}"


