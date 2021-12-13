from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_action_listing")
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'images', blank=True, null=True)
    comments = models.ManyToManyField('Comment', blank=True, related_name="comment_on_auction")
    latest_bid = models.ForeignKey('Bid', on_delete=models.CASCADE, related_name="if_bid_is_last")
    date = models.DateTimeField(default=timezone.now)
    close = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_by_user")
    bid = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="aunction_bid")

    def __str__(self):
        return f"{self.bid} ({self.user})"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_by_user")
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s %s' % ({self.user.username}, {self.date})

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist")
    auction = models.ManyToManyField(Auction, blank=True, related_name="acution_watchlist")

    def __str__(self):
        return f"{self.user}"

