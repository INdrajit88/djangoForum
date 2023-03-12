from django import forms

from .models import Post,Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_content',
            'post_tags',
            'post_category'
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment_content',
            'comment_post'
        ]