from django.contrib import admin

# Register your models here.
from .models import Auction, Comment, Category, Bid, Watchlist, User

admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Watchlist)
admin.site.register(User)