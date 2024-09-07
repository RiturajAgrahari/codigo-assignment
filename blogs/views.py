from django.shortcuts import render, redirect
from .forms import LoginForm, CustomUserCreationForm, BlogForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Blog, Comment, Tag
import datetime
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.


@login_required(login_url="/login")
def index(request):
    """
     HOME PAGE TO SEE LIST VIEW OF BLOGS
     PAGINATION OF % BLOGS ON EACH PAGE
    """
    if request.method == "POST":
        search_text = request.POST.get("search")
        search_tag = request.POST.get("tag")
        sort_by = request.POST.get("sort_by")
        blogs_list = Blog.objects.all().order_by("-publish_on")
        if search_text:
            blogs_list = blogs_list.filter(title__icontains=search_text)
        if search_tag:
            blogs_list = blogs_list.filter(tags__name__icontains=search_tag)
        if sort_by:
            if sort_by == "likes":
                a = sorted(blogs_list, key=lambda obj: Blog.number_of_likes(obj))
                blogs_list = a[::-1]
            else:
                blogs_list = blogs_list.order_by(f"-{sort_by}")

        last_page = len(blogs_list) // 5
        paginator = Paginator(blogs_list, 5)
        page_number = request.GET.get("page")
        tags = Tag.objects.all()

        try:
            page_obj = paginator.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "blogs": page_obj,
            "last_page": last_page,
            "page_number": 1 if not page_number else page_number,
            "tags": tags,
            "sort_by": sort_by
        }

        return render(request, "authentication/index.html", context=context)
    else:
        blogs_list = Blog.objects.all().order_by("-publish_on")
        last_page = len(blogs_list) // 5
        paginator = Paginator(blogs_list, 5)
        page_number = request.GET.get("page")
        tags = Tag.objects.all()

        try:
            page_obj = paginator.get_page(page_number)  # returns the desired page object
        except PageNotAnInteger:
            # if page_number is not an integer then assign the first page
            page_obj = paginator.page(1)
        except EmptyPage:
            # if page is empty then return last page
            page_obj = paginator.page(paginator.num_pages)

        context = {
            "blogs": page_obj,
            "last_page": last_page,
            "page_number": 1 if not page_number else page_number,
            "tags": tags
        }

        return render(request, "authentication/index.html", context=context)


@login_required(login_url="/login")
def detail_view(request, id):
    user = request.user.username
    blog = Blog.objects.all().filter(id__iexact=id)
    comments = Comment.objects.all().filter(post=id).order_by("-created_on")

    likes_connected = get_object_or_404(Blog, id=id)
    liked = False
    if likes_connected.likes.filter(id=request.user.id).exists():
        liked = True

    context = {
        "blogs": blog,
        "username": user,
        "comments": comments,
        "post_is_liked": liked
    }
    return render(request, "authentication/detail.html", context=context)


@login_required(login_url="/login")
def blog_category(request, category):
    posts = Blog.objects.filter(
        tags__name__contains=category
    ).order_by("-publish_on")
    context = {
        "category": category,
        "blogs": posts,
    }
    return render(request, "authentication/category.html", context)


@login_required(login_url="/login")
def author_blog(request, author):
    username = User.objects.all().filter(username=author)[0]
    posts = Blog.objects.filter(
        author=username
    ).order_by("-publish_on")
    context = {
        "author": author,
        "blogs": posts,
    }
    return render(request, "pages/author.html", context)


def BlogPostLike(request, pk):
    post = get_object_or_404(Blog, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog', args=[str(pk)]))


def comment_like(request, pk):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    blog_id = request.POST.get("blog_id")
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog', args=[str(blog_id)]))


@login_required(login_url="/login")
def comment(request, id):
    if request.method == "POST":
        blog = Blog.objects.all().filter(id=id)[0]
        comment = request.POST.get("comment")
        Comment.objects.create(
            author=request.user.username,
            body=comment,
            created_on=datetime.datetime.now(),
            post=blog
        )
        messages.add_message(request, messages.SUCCESS, "comment added successfully!")
        return redirect(f"/blogs/{id}")
    else:
        return redirect("/")


def post(request):
    if request.method == "POST":
        form = BlogForm(request.POST)


        author = User.objects.all().filter(pk=request.POST["author"])[0]

        incomplete_form = form.save(commit=False)
        incomplete_form.author = author
        incomplete_form.save()

        return redirect("/")
    else:
        form = BlogForm()
        context = {
            "post_form": form
        }
        return render(request, template_name="pages/post.html", context=context)


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                message = "Authentication Successful"
                messages.add_message(request, messages.SUCCESS, message)
                return redirect("home")

            else:
                message = "Invalid Credentials"
                messages.add_message(request, messages.ERROR, message)
                return redirect("/login")

        else:
            form = LoginForm()
            return render(request, "authentication/login.html", context={"message": "Invalid Input!", "form": form})

    else:
        if request.user.is_authenticated:
            return redirect("home")
        else:
            form = LoginForm()
            return render(request, "authentication/login.html", context={"form": form})


def logout_view(request):
    logout(request)
    return redirect("/login")


def signin(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            message = "Sign in Successful!"
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("/")

        else:
            message = (list(form.error_messages.values())[0])
            messages.add_message(request, messages.ERROR, message)
            return redirect("/signin")

    else:
        if request.user.is_authenticated:
            return redirect("home")
        else:
            form = CustomUserCreationForm()
            return render(request, "authentication/signin.html", context={"form": form})



