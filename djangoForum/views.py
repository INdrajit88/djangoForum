
from django.shortcuts import redirect,render
from  posts.models import Category,Post
def home(request):
    posts = Post.objects.all().order_by('post_created_at')
    categories = Category.objects.all().order_by('category_created_at')
    favourite_posts = Post.objects.order_by('post_likes')[:5]# Only getting the top 5 liked posts
    post_count = Post.objects.all().count()
    context = {
        "posts":posts,
        "categories": categories,
        "post_count" : post_count,
        "favourite_posts":favourite_posts
    }
    return render(request,'home.html',context)

def search(request):
    search_query = request.GET['search_query']
    posts = Post.objects.filter(post_content__icontains=search_query,post_title__icontains=search_query)
    context = {
        "posts":posts,
        "search_query":search_query
    }
    return render(request,'search.html',context)