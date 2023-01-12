from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    startBid = models.DecimalField(max_digits=100, decimal_places=2)
    imageURL = models.URLField()
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}: {self.description}, {self.startBid}"

    class Meta:
        ordering = [F("id").desc()]


class Bids(models.Model):
    pass

class Comments(models.Model):
    pass