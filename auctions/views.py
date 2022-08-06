from queue import Empty
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required


from .models import User, Auction, Comment, Bid

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


def index(request):
    return render(request, "auctions/index.html", {
        "auctions" : Auction.objects.filter(status=True),        
    })


def login_view(request):
    # if request.method == "GET":
    #     # try: 
    #     #     next = request.GET["next"]
    #     # except 
    #     if request.GET["next"]:   
    #         return render(request, "auctions/login.html",{
    #             "next":request.GET["next"] 
    #         })        
    #     else:
    #         return render(request, "auctions/login.html")
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
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# @login_required(login_url='/login')
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
    return render(request, "auctions/detail.html",{
            'auction': auction,
            'comments': auction.comments.all(),
            'categories': auction.categories.all(),
            'bid' : auction.bids.last(),
            'commentForm': NewCommentForm(user=request.user, auction = auction.id)
            })

def comment_post(request, auction_id):
    if request.method == "POST":
        auction = Auction.objects.get(pk=int(auction_id))
        form = NewCommentForm(request.POST, user=request.user, auction = auction)
        # auction = Auction.objects.get(pk=auction_id)
        # comment = Comment.objects        
        # auction.comments.add("test", request.user)
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