from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "tags"

    def __str__(self):
        return self.name


class Blog(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    description = models.TextField()
    publish_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='blogpost_like', blank=True)
    tags = models.ManyToManyField("Tag", related_name="blogs")

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='comment_like', blank=True)
    post = models.ForeignKey("Blog", on_delete=models.CASCADE)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.author} on '{self.post}'"
