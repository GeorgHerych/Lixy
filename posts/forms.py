from django import forms

from posts.models import Post

from django.utils import timezone

class CreatePostForm(forms.ModelForm):
    images = forms.FileField(
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'images']

    def save(self, commit=True, user=None):
        post = super().save(commit=False)

        post.pub_date = timezone.now()

        if user:
            post.member = user

        if commit:
            post.save()

        return post

class EditPostForm(forms.ModelForm):
    images = forms.FileField(
        required=False
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'images']

    def save(self, commit=True, user=None):
        post = super().save(commit=False)

        post.pub_date = timezone.now()

        if user:
            post.member = user

        if commit:
            post.save()

        return post