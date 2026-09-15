from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name="blogposts")
    likes = models.ManyToManyField(to=get_user_model(), related_name="blogpost_likes", blank=True)
    picture = models.ImageField(upload_to="pictures/", blank=True, null=True)


    def get_absolute_url(self):
        return reverse("detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.title} {self.description[:20]}"


# class BlogPostLikes(models.Model):
#     post = models.ForeignKey(to=BlogPost, on_delete=models.CASCADE)
#     user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ("post", "user")


class ApprovedCommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state=Comment.STATE_CHOICES_APPROVED)


class CommentManager(models.Manager):
    def get_approved_comments(self):
        return self.get_queryset().filter(state=Comment.STATE_CHOICES_APPROVED)

    def get_rejected_comments(self):
        return self.get_queryset().filter(state=Comment.STATE_CHOICES_REJECTED)

    def get_pending_comments(self):
        return self.get_queryset().filter(state=Comment.STATE_CHOICES_PENDING)
        


class Comment(models.Model):
    STATE_CHOICES_APPROVED = "a"
    STATE_CHOICES_REJECTED = "r"
    STATE_CHOICES_PENDING = "p"
    STATE_CHOICES = (
        (STATE_CHOICES_APPROVED, "تایید شده"),
        (STATE_CHOICES_REJECTED, "رد شده"),
        (STATE_CHOICES_PENDING, "در انتظار تایید"),
    )
    name = models.CharField(max_length=255, verbose_name="نام")
    email = models.EmailField(null=True, blank=True, verbose_name="ایمیل")
    address = models.TextField(blank=True, verbose_name="آدرس")
    city = models.CharField(max_length=255, blank=True, verbose_name="شهر")
    province = models.CharField(max_length=255, blank=True, verbose_name="استان")
    zip_code = models.CharField(max_length=11, blank=True, verbose_name="کد پستی")
    hide_name = models.BooleanField(default=True, verbose_name="مخفی کردن نام")
    comment = models.TextField(verbose_name="نظر")
    post = models.ForeignKey(to=BlogPost, on_delete=models.CASCADE, verbose_name="پست", related_name="comments")
    datetime_created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    datetime_modified = models.DateTimeField(auto_now=True, verbose_name="زمان آخرین ویرایش")
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=STATE_CHOICES_PENDING, verbose_name="وضعیت کامنت")

    objects = models.Manager()
    my_objects = CommentManager()