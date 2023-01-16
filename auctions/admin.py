from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(AuctionListing)
admin.site.register(Bids)
# admin.site.register(WatchList)
admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Comments)