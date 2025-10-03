from django import forms

from django.utils import timezone
from comments.models import Comment

class CreateCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment'}), label='')

    class Meta:
        model = Comment
        fields = ('content', )
        
    def save(self, commit=True, user=None, post=None):
        comment = super().save(commit=False)

        comment.pub_date = timezone.now()

        if user:
            comment.member = user

        if post:
            comment.post = post

        if commit:
            comment.save()

        return comment

class EditCommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))

    class Meta:
        model = Comment
        fields = ('content', )