
from django.urls import path
from . import views
urlpatterns = [
    # Post Routes
    path("show_post/<slug:post_slug>",views.show_post,name="show_post"),
    path("create",views.create_post,name="create_post"),
    path("like_post/<slug:post_slug>",views.like_post,name="like_post"),
    # Comment Routes
    path("comment/create",views.create_comment,name='create_comment')

]
