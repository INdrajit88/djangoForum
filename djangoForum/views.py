
from django.shortcuts import redirect,render
from  posts.models import Category,Post
from django.contrib.auth.models import User
from django.db.models import Count



def home(request):
    posts = Post.objects.all().order_by('-post_created_at') #Getting the posts based on when they were created
    
    categories = Category.objects.all().order_by('category_created_at') #Fetching the categories based on when they were created
    favourite_posts = Post.objects.order_by('-post_view_count')[:5]# Only getting the top viewed posts
    post_count = Post.objects.all().count() #Counting the number of posts
    user_count  = User.objects.all().count() # Counting the total number of users
    category_count = Category.objects.all().count() # Counting the total number of categories
    context = {
        "posts":posts,
        "categories": categories,
        "post_count" : post_count,
        "favourite_posts":favourite_posts,
        "user_count": user_count,
        "category_count": category_count,
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