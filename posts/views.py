from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import PostForm
from .models import Comment, Post
from django.contrib.auth.decorators import login_required



def viewed_by_session_count(request, obj):
    session_key = 'viewed_{}'.format(obj.post_id)
 
    if not request.session.get(session_key, False):
        obj.post_view_count += 1
        obj.save(update_fields=['post_view_count'])
        request.session[session_key] = True


def show_post(request, post_slug):
    post = Post.objects.filter(post_slug=post_slug).first()
    if post:
   
        post_comments = Comment.objects.filter(
            comment_post=post.post_id).order_by('comment_created_at')
        post_liked = False
        post_delete=False
        if request.user.is_authenticated:
            if post.post_created_by == request.user:
                post_delete=True

            if post.post_likes.filter(id=request.user.id).exists():
                post_liked = True

        context = {
            "post": post,
            "post_liked": post_liked,
            "post_comments": post_comments,
            "post_delete": post_delete
        }
        viewed_by_session_count(request, post)
        return render(request, "post/show.html", context)
    else:
        return redirect("home")

@login_required(login_url="/")
def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        form.instance.post_created_by = request.user
        # form.instance.post_slug = slugify(request.post_title)

        new_post.save()
        form.save_m2m()
        messages.success(request, "Post created succesfully")
        return redirect("home")
    context = {
        "form": form
    }
    return render(request, 'post/create.html', context)


def create_comment(request):
    if request.method == "POST":
        post_slug = request.POST['post_slug']
        comment_post = Post.objects.get(post_slug=post_slug)
        if comment_post:
            comment_content = request.POST['comment_content']
            comment_user = request.user
            new_comment = Comment(comment_content=comment_content,
                                  comment_user=comment_user, comment_post=comment_post)
            new_comment.save()

            return redirect("show_post", post_slug)

    return redirect("home")

def show_category_posts(request,category_id):
    # Shows the Posts in a category based on category Id
    posts = Post.objects.filter(post_category=category_id).order_by("-post_created_at")
    context = {
        "posts":posts
    }
    return render(request,"category/show.html",context)

def like_post(request, post_slug):
    post = Post.objects.get(post_slug=post_slug)
    if request.method == "POST" and post:
        if request.user.is_authenticated:
            user = request.user
            if post.post_likes.filter(id=user.id).exists():
                post.post_likes.remove(user)
                return redirect("show_post", post_slug)
            else:
                post.post_likes.add(user)
                return redirect("show_post", post_slug)
def delete_post(request):
    if request.method == "POST":
        post_slug = request.POST['post_slug']

        if request.user.is_authenticated:
            post = Post.objects.filter(post_slug=post_slug).first()
            if post.post_created_by == request.user:
                post.delete()
                messages.success(request,"Successfully deleted the post")
                return redirect("home")
            else:
                messages.error(request,"Something went wrong when deleting the post")
    return redirect("home")
        