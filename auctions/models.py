from pyexpat import model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"
class Category(models.Model):
    text = models.CharField(max_length=64)        
class Auction(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.FloatField()        
    categories = models.ManyToManyField(Category)
    urlimg = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.title} started at {self.start_bid} now we are here "
class Comment(models.Model):
    text = models.TextField()
    date = models.DateField(auto_now_add=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    def __str__(self):
        return f"{self.text} by {self.user} on {self.date}"

class Bid(models.Model):
    price = models.FloatField()
    date = models.DateField(auto_now_add=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)    
    user = models.ForeignKey(User, on_delete=models.PROTECT)   
    def __str__(self):
        return f"{self.price} ({self.user})"
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ManyToManyField(Auction, related_name='watchlist', blank=True)
