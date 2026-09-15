from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import BlogPost, Comment
from .forms import BlogPostCommentForm


class BaseListView(generic.ListView):
    model = BlogPost
    template_name = "index.html"
    context_object_name = "posts"
    paginate_by = 10
    queryset = BlogPost.objects.all().order_by("-datetime_modified")


class Home(BaseListView):
    pass


class RecentPosts(BaseListView):
    def get_queryset(self):
        return self.queryset[:5]
        return super().get_queryset()[:5]


class Favorites(LoginRequiredMixin, BaseListView):
    def get_queryset(self):
        user = self.request.user
        return user.blogpost_likes.all().order_by("-datetime_modified")


class MyPosts(LoginRequiredMixin, BaseListView):
    template_name = "my_posts.html"
    def get_queryset(self):
        user = self.request.user
        object = user.blogposts
        for obj in object.all():
            print("Author : ", obj.author)
        # if self.model.objects.filter(author=user):
        #     print(user.blogposts.author)
        return self.model.objects.filter(author=user).all().order_by("-datetime_modified")


class Add(LoginRequiredMixin, generic.CreateView):
    model = BlogPost
    template_name = "add.html"
    context_object_name = "post"
    fields = ["title", "description", "picture"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = "add"
        return context

    def post(self, request, *args, **kwargs):
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


class Detail(generic.DetailView):
    model = BlogPost
    context_object_name = "post"
    template_name = "detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = BlogPostCommentForm()
        post = self.get_object()
        context["comments"] = Comment.my_objects.get_approved_comments().filter(post=post)
        # context["comments"] = Comment.objects.filter(post=post, state=Comment.STATE_CHOICES_APPROVED)
        # context["comments"] = post.comments.filter(state=Comment.STATE_CHOICES_APPROVED)
        return context

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        post = self.get_object()
        if action == "comment":
            form = BlogPostCommentForm(request.POST)

            if form.is_valid() and request.user.is_authenticated:
                form = form.save(commit=False)
                form.post = post
                form.save()
                form = BlogPostCommentForm()
                messages.success(request, f"نظر شما با موفقیت دریافت شد و پس از تایید مدیریت در سایت نمایش داده خواهد شد.")
            else:
                messages.error(request, f"لطفا فرم را درست پر کنید")
                return redirect("login")    
        elif action == "like":
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                messages.success(request, f"لایک پست {post.title} با موفقیت حذف شد.")
            else:
                post.likes.add(request.user)
                messages.success(request, f"پست {post.title} با موفقیت به لیست علاقه مندی ها اضافه شد.")
        return super().get(request, *args, **kwargs)


class Delete(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = BlogPost
    context_object_name = "post"
    template_name = "delete.html"
    success_url = reverse_lazy("home")

    def test_func(self):
        user = self.request.user
        post = self.get_object()
        return user == post.author


class Update(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = BlogPost
    template_name = "add.html"
    context_object_name = "post"
    fields = ["title", "description", "picture"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_name"] = "update"
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        title = request.POST.get("title")
        description = request.POST.get("description")
        picture = request.FILES.get("picture")
        post.title = title
        post.description = description
        post.picture = picture
        post.save()
        return redirect(post.get_absolute_url())

    def test_func(self):
        user = self.request.user
        post = self.get_object()
        return user == post.author
