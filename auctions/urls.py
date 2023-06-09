from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listings/<int:listing_id>", views.listings, name="listings"),
    path("newBid/<int:listing_id>", views.newBid, name="newBid"),
    path("closeAuction/<int:listing_id>", views.closeAuction, name="closeAuction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.categoryPage, name="categoryPage"),
    path("comments/<int:listing_id>", views.comments, name="comments"),
]
