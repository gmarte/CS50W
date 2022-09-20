import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.all()
    })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def profile(request, user_id):
    profile_user = User.objects.get(pk=user_id)
    user = request.user
    if user.is_authenticated:
        follower = profile_user.followers.filter(id=user.id).exists()
    else:
        follower = False
    if request.method == "POST" and user.id != profile_user.id:
        if follower:
            user.following.remove(profile_user.id)
            follower = False
        else:
            user.following.add(profile_user.id)
            follower = True

    return render(request, "network/profile.html", {
        "profile": profile_user,
        "follower": follower,
        "posts": Post.objects.filter(creator=profile_user).all()
    }) 

@csrf_exempt
@login_required
def posts(request, post_id=''):
    user = request.user
    if request.method == "POST":
        description = request.POST["description"]
        if description:
            post = Post(description=description, creator=user)
            post.save()
        else:
            return render(request, "network/index.html", {
                "message": "You must complete the description."
            })
        return HttpResponseRedirect(reverse("index"))
    elif request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        data = json.loads(request.body)
        if data.get("like") is not None:
            if (user.post_likes.filter(pk=post_id).exists()):
                post.likes.remove(user)
                like_post = False
            else: # add the like to the post 
                post.likes.add(user)
                like_post = True
        likes_count = post.likes_count
        return JsonResponse({"likes_count": likes_count, "like_post":like_post}, status=200)
        # return HttpResponse(status=204)    
