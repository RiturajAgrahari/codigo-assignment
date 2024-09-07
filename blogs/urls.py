from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("blogs", views.index, name="blogs"),
    path("blogs/<int:id>", views.detail_view, name="blog"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("authors/<author>/", views.author_blog, name="author_blog"),
    path('blogpost-like/<int:pk>', views.BlogPostLike, name="blogpost_like"),
    path('comment-like/<int:pk>', views.comment_like, name="comment_like"),
    path("comment/<id>/", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signin", views.signin, name="signin"),
]