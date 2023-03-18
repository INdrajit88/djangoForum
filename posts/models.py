from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django.utils.crypto import get_random_string


# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=60,default='')
    category_description = models.TextField()
    category_thumbnail = models.ImageField(upload_to="thumbnails/category",null=True)
    category_slug = models.SlugField(unique=True,null=True)
    category_post_number = models.PositiveBigIntegerField(default=0)
    category_created_at = models.DateTimeField(auto_now_add=True)
    category_tags = TaggableManager()
    category_created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.category_name


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_title = models.CharField(max_length=50)
    post_content = models.TextField()
    post_slug = models.SlugField(unique=True,null=True)
    post_tags = TaggableManager()
    post_likes = models.ManyToManyField(User,related_name='post_likes')
    post_created_at = models.DateTimeField(auto_now_add=True)
    post_created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    post_category = models.ForeignKey(Category,on_delete=models.CASCADE)
    post_view_count = models.IntegerField(default=0)
    def __str__(self):
        return self.post_content
    # When saving the post automatically add the create a slug based on post title so that user dont have to enter slug manualy
    def save(self, *args, **kwargs):
        value = self.post_title 
        self.post_slug = slugify(value, allow_unicode=True) 
        super().save(*args, **kwargs)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_content = models.TextField()
    comment_post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    comment_created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.comment_content