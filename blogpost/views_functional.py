from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import BlogPost, Comment
from .forms import BlogPostCommentForm
from .decorators import post_owner_required


def home(request):
    posts_list = BlogPost.objects.all().order_by("-datetime_modified")
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {"posts": posts}
    return render(request, "index.html", context)


@login_required
def add(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        description = request.POST.get("description")
        picture = request.FILES.get("picture")
        p = BlogPost.objects.create(
            title=title,
            description=description,
            author=user,
            picture=picture,
        )
        return redirect(p.get_absolute_url())
    context = {"page_name": "add"}
    return render(request, "add.html", context)


def detail(request, pk):
    # post = BlogPost.objects.get(pk=pk)
    post = get_object_or_404(BlogPost, pk=pk)
    comments = Comment.objects.filter(post=post)
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email", None)
        address = request.POST.get("address", "")
        city = request.POST.get("city", "")
        province = request.POST.get("province", "")
        zip_code = request.POST.get("zip_code", "")
        hide_name = request.POST.get("hide_name")
        hide_name = True if hide_name else False
        comment = request.POST.get("comment")
        Comment.objects.create(
            name=name,
            email=email,
            address=address,
            city=city,
            province=province,
            zip_code=zip_code,
            hide_name=hide_name,
            comment=comment,
            post=post,
        )
    context = {"post": post, "comments": comments}
    return render(request, "detail.html", context)


def detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    # comments = Comment.objects.filter(post=post, state=Comment.STATE_CHOICES_APPROVED)
    comments = post.comments.filter(state=Comment.STATE_CHOICES_APPROVED)
    form = BlogPostCommentForm()
    if request.method == "POST":
        action = request.POST.get("action")
        if action=="comment":
            form = BlogPostCommentForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.post = post
                form.save()
                form = BlogPostCommentForm()
        elif action=="like":
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
        
    context = {"post": post, "comments": comments, "form": form}
    return render(request, "detail.html", context)


def test_func(user, *args, **kwargs):
    pk = kwargs.get("pk")
    post = get_object_or_404(BlogPost, pk=pk)
    return user==post.author


@post_owner_required
def delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method=="POST":
        if request.user == post.author:
            post.delete()
            return redirect("home")
    context = {"post": post}
    return render(request, "delete.html", context)


@post_owner_required
def update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method=="POST":
        if request.user == post.author:
            title = request.POST.get("title")
            description = request.POST.get("description")
            picture = request.FILES.get("picture")
            post.title = title
            post.description = description
            post.picture = picture
            post.save()
            return redirect(post.get_absolute_url())
    context = {"post": post, "page_name": "update"}
    return render(request, "add.html", context)


def recent_posts(request):
    posts = BlogPost.objects.all().order_by("-datetime_modified")[:5]
    context = {"posts": posts}
    return render(request, "index.html", context)


@login_required
def favorites(request):
    user = request.user
    posts_list = user.blogpost_likes.all().order_by("-datetime_modified")
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {"posts": posts}
    return render(request, "index.html", context)


@login_required
def my_posts(request):
    user = request.user
    posts_list = user.blogposts.all().order_by("-datetime_modified")
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {"posts": posts}
    return render(request, "index.html", context)