from argparse import Action
from queue import Empty
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, reset_queries
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required


from .models import Category, User, Auction, Comment, Bid, Watchlist

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ['auction', 'user']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control-lg'}),
        }   
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        self._auction = kwargs.pop('auction')
        super(NewCommentForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        inst = super(NewCommentForm, self).save(commit=False)
        inst.user = self._user
        inst.auction = self._auction
        if commit:
            inst.save()
            self.save_m2m()
        return inst
class NewAuctionForm(forms.ModelForm):    
    class Meta:
        model = Auction
        fields = "__all__"
        exclude = ['status','creator']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'urlimg': forms.TextInput(attrs={'class': 'form-control'}),
            'start_bid': forms.TextInput(attrs={'class': 'form-control'}),        
            # 'creator': forms.HiddenInput(),
            # 'categories': forms.ModelMultipleChoiceField(),            
            # 'categories': forms.ChoiceField(attrs={'class': 'form-control'}),            
        }
    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super(NewAuctionForm, self).__init__(*args, **kwargs)
    def save(self, commit=True):
        inst = super(NewAuctionForm, self).save(commit=False)
        inst.creator = self._user
        if commit:
            inst.save()
            self.save_m2m()
        return inst
# Region Auction
@login_required
def create(request):
    if request.method == 'POST':
        form = NewAuctionForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html",{
            'form': form
            })            

    else:        
        return render(request, "auctions/create.html",{
            'form': NewAuctionForm(user=request.user)
            })        
def auction_view(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)    
    watch_listed = False
    # verify watchlist
    if request.user.is_authenticated:
        user = request.user            
        if auction.watchlist.filter(user=user).count() > 0:
            watch_listed = True
    # verify status
    if auction.status == False:
        winner = auction.bids.last().user
    else:
        winner = None
    return render(request, "auctions/detail.html",{
            'auction': auction,
            'comments': auction.comments.all().order_by('-date'),
            'categories': auction.categories.all(),
            'bid' : auction.bids.last(),
            'winner': winner,
            'watch_listed': watch_listed,
            'commentForm': NewCommentForm(user=request.user, auction = auction.id)
            })
def auction_close(request, auction_id):
    if request.method == "POST":
        user = request.user
        auction = Auction.objects.get(pk=int(auction_id))
        auction.status = False
        print(auction.status)
        auction.save()
    return HttpResponseRedirect(reverse("view", args=(auction.id,)))
# endregion
@login_required
def comment_post(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=int(auction_id))
        form = NewCommentForm(request.POST, user=request.user, auction = auction)        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("view", args=(auction.id,)))
        else:
            return render(request, "auctions/detail.html",{
            'auction': auction,
            'comments': auction.comments.all(),
            'bid' : auction.bids.last(),
            'commentForm': form
            })             
def index(request):
    return render(request, "auctions/index.html", {
        "auctions" : Auction.objects.all(),        
    })
@login_required
def watchlist_view(request):
    user = request.user
    auctions = user.watchlist.first().auction.all()
    return render(request, "auctions/watchlist.html", {
        "auctions" : auctions,        
    })
@login_required
def watchlist_add(request,auction_id):
    if request.method == 'GET':        
        auction = Auction.objects.get(pk=int(auction_id))    
        user = request.user
        wl = Watchlist.objects.get(user=user)         
        if wl.auction.filter(pk = auction.id).count() > 0:                                    
            wl.auction.remove(auction)
        else:
            wl.auction.add(auction)
            wl.save()                                                
        return HttpResponseRedirect(reverse("view", args=(auction.id,)))
@login_required
def bid(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=int(auction_id))    
        user = request.user
        watch_listed = False
        if auction.watchlist.filter(user=user).count() > 0:
            watch_listed = True
        # recieved a bid
        if request.POST["bid"]:
            userBid = float(request.POST["bid"])              
        else:            
            userBid = 0
        if auction.bids.last():
            highiestBid = auction.bids.last().price
        else:
            highiestBid = 0        
        # verified that the bid is greater than the initial bid factor                
        if userBid > highiestBid and highiestBid > 0:
            bid = Bid(price=userBid, user=user, auction=auction)
            bid.save()
            bidMessage = "You have taken the lead!"
        elif userBid > auction.start_bid and highiestBid == 0:
            bid = Bid(price=userBid, user=user, auction=auction)
            bid.save()
            bidMessage = "New highest bidder!"
        else:
            bidMessage = "Your bid must be higher!"
            return render(request, "auctions/detail.html",{
            'auction': auction,
            'comments': auction.comments.all().order_by('-date'),
            'categories': auction.categories.all(),
            'bid' : auction.bids.last(),
            'watch_listed': watch_listed,
            'bidMessage': bidMessage,
            'commentForm': NewCommentForm(user=request.user, auction = auction.id)
            })

        return HttpResponseRedirect(reverse("view", args=(auction.id,)))                
# Region Categories
def categories_view(request):
    return render(request, "auctions/categories.html",{
        'categories': Category.objects.all()
    })
def categories_detail(request, category_id):
    auction = Auction.objects.filter(categories__pk=category_id)
    return render(request, "auctions/categories_detail.html",{
        'auctions': auction
    })
# endregion    
# region User Auth
def login_view(request):    
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]        
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            w = Watchlist(user=user)
            w.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")  
# endregion                  