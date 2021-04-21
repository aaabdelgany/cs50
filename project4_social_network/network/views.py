from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import User,Post,Follow,Like
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


class NewPostForm(forms.Form):
    content=forms.CharField(label="New Post",widget=forms.Textarea)


@csrf_exempt
def index(request):
    if request.method=="POST":
        data=json.loads(request.body)
        edit_post=Post.objects.get(id=data.get("id"))
        edit_post.content=data.get("content")
        edit_post.save()
        return JsonResponse({"success": "POST request required."}, status=201)
        return JsonResponse({"success": "POST request required."}, status=201)
    page=request.GET.get('page',1)
    all_posts=Post.objects.order_by('-timestamp')
    paginator=Paginator(all_posts,10)
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html",{
        "Posts":posts,
        "myuser":request.user.username,
        "form":NewPostForm()
    })

@login_required
@csrf_exempt
def follow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    data=json.loads(request.body)
    follower=User.objects.get(username=data.get("follower"))
    followed=User.objects.get(username=data.get("followed"))
    try:
        follow=Follow.objects.get(follower=follower, followed=followed)
        follow.delete()
    except Follow.DoesNotExist:
        print('fail')
        follow=False
        new_follow=Follow(follower=follower,followed=followed)
        new_follow.save()
    return JsonResponse({"follows":len(Follow.objects.filter(follower=followed)),"followed":len(Follow.objects.filter(followed=followed))}, status=201)
def user(request,username):
    self_req=False
    if username==request.user.username:
        self_req=True
    try:
        requester=User.objects.get(username=request.user.username)
        req_user=User.objects.get(username=username)
        try:
            Follow.objects.get(follower=requester, followed=req_user)
            follow=True
        except Follow.DoesNotExist:
            follow=False
        user_follows=len(Follow.objects.filter(follower=req_user))
        user_followed=len(Follow.objects.filter(followed=req_user))
        return render(request,"network/user.html",{
            "Posts":reversed(req_user.posts.all()),
            "self":self_req,
            "follows":follow,
            "follower":requester,
            "followed":req_user,
            "user_follows":user_follows,
            "user_followed":user_followed
        })
    except User.DoesNotExist:
        req_user=User.objects.get(username=username)
        user_follows=len(Follow.objects.filter(follower=req_user))
        user_followed=len(Follow.objects.filter(followed=req_user))
        return render(request,"network/user.html",{
            "Posts":reversed(req_user.posts.all()),
            "user_follows":user_follows,
            "user_followed":user_followed
        })
@csrf_exempt
@login_required
def like(request):
    data=json.loads(request.body)
    post=Post.objects.get(id=data.get("id"))
    liker=User.objects.get(username=request.user.username)
    if request.method=="POST":
        try:
            old_like=Like.objects.get(post=post,username=liker)
            old_like.delete()
            post.num_likes=post.num_likes-1
            post.save()
        except Like.DoesNotExist:
            new_like=Like(post=post,username=liker)
            new_like.save()
            post.num_likes=post.num_likes+1
            post.save()
        return JsonResponse({"num":post.num_likes}, status=201)
    # likes=len(Like.objects.filter(post=post))
    # return JsonResponse({"likes":likes},status=200)

@login_required
@csrf_exempt
def user_like(request):
    data=json.loads(request.body)
    post=Post.objects.get(id=data.get("id"))
    liker=User.objects.get(username=request.user.username)
    try:
        Like.objects.get(post=post,username=liker)
        print('true')
        return JsonResponse({"likes":True}, status=201)

    except Like.DoesNotExist:
        print('false')
        return JsonResponse({"likes":False}, status=201)




@login_required
def following(request):
    follower=User.objects.get(username=request.user.username)
    follows=Follow.objects.filter(follower=follower)
    posts=[]
    for follow in follows:
        followed=follow.followed
        for post in followed.posts.all():
            posts.append(post)
            #print(post)
    page=request.GET.get('page',1)

    posts=sorted(posts,key=lambda post:post.timestamp,reverse=True)
    paginator=Paginator(posts,10)
    try:
        follow_posts=paginator.page(page)
    except PageNotAnInteger:
        follow_posts = paginator.page(1)
    except EmptyPage:
        follow_posts = paginator.page(paginator.num_pages)
    return render(request, "network/index.html",{
        "Posts":follow_posts,
        "form":NewPostForm()
    })
def new(request):
    if request.method=="POST":
        form=NewPostForm(request.POST)
        print(request.user.username)
        if form.is_valid():
            content=form.cleaned_data["content"]
            new_post=Post(username=User.objects.get(username=request.user.username),content=content,num_likes=0)
            new_post.save()

    return HttpResponseRedirect(reverse("index"))
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
