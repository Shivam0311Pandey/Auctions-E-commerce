from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("newlisting/addCategory", views.addCategory, name="addCategory"),
    path("category/<str:category>", views.viewCategory, name="viewCategory"),
    path("auction/<int:auctionId>", views.viewAuction, name="viewAuction"),
    path("deleteListing/<int:auctionId>", views.deleteListing, name="deleteListing"),
    path("addComment/<int:auctionId>", views.addComment, name="addComment"),
    path("auction/deleteComment/<int:commentId>", views.deleteComment, name="deleteComment"),
    path("auction/placeBid", views.placeBid, name="placeBid"),
    path("closeLisitng/<int:auctionId>", views.closeLisitng, name="closeLisitng"),
    path("myListing", views.myListing, name="myListing"),
    path("auction/addremoveWatchlist/<int:auctionId>", views.addremoveWatchlist, name="addremoveWatchlist"),
    path("watchlist", views.viewWatchlist, name="viewWatchlist")
]
