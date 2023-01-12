from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class User(AbstractUser):
    pass

class Bids(models.Model):
    bid = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return f"{self.bid}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    imageURL = models.URLField()
    category = models.CharField(max_length=100)
    bid = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.title}: {self.description}, {self.bid}"

    class Meta:
        ordering = [F("id").desc()]


class WatchList(models.Model):
    watchedAuctions = models.ForeignKey(AuctionListing, blank=True, related_name="watchedAuctions")

    def __str__(self):
        return f"{self.watchedAuctions}"


class Comments(models.Model):
    pass