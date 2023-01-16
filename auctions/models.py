from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    imageURL = models.URLField(blank=True)
    bid = models.DecimalField(max_digits=100, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userListing")

    active = models.BooleanField(default=True)
    watchlist = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} | {self.description} | {self.bid}"

    class Meta:
        ordering = [F("id").desc()]


class Bids(models.Model):
    bid = models.DecimalField(max_digits=100, decimal_places=2, blank=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userBids")

    def __str__(self):
        return f"{self.user}"


class Categories(models.Model):
    category = models.CharField(max_length=100, blank=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="category")

    def __str__(self):
        return f"{self.category}"


class Comments(models.Model):
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    listing = models.ManyToManyField(AuctionListing, blank=True, related_name="comments")

    def __str__(self):
        return f"{self.comment}"
