from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group

from .forms import LoginForm, RegistrationForm, PostForm
from .models import Post


@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        if post_id:
            print(f"Deleting post {post_id}...")
            post = Post.objects.filter(id=post_id).first()
            if post and (
                post.author == request.user or request.user.has_perm("main.delete_post")
            ):
                post.delete()

    return render(request, "main/home.html", {"posts": posts})


def ban_user(request, pk):
    user_id = request.POST.get("user-id")
    if user_id:
        print(f"Banning user {user_id}...")
        user = User.objects.get(id=user_id)
        if user and request.user.is_staff:
            default_group = Group.objects.get(name="default")
            if user in default_group.user_set.all():
                default_group.user_set.remove(user)
                print(f"User {user.username} removed from {default_group.name} group.")
            mod_group = Group.objects.get(name="mod")
            if user in mod_group.user_set.all():
                mod_group.user_set.remove(user)
                print(f"User {user.username} removed from {mod_group.name} group.")
        else:
            print("duh")
    return redirect("/home")


@login_required(login_url="/login")
@permission_required("main.add_post", login_url="/login", raise_exception=True)
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, "main/create_post.html", {"form": form})

    return render(request, "main/create_post.html")


def sign_up(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegistrationForm()
    return render(request, "registration/sign_up.html", {"form": form})


# def login(request):
#     login_form = LoginForm(request.POST or None)
#     return render(request, "registration/login.html", {"form": login_form})
#     # , {"form": login_form}
