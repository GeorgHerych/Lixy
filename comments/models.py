from django.db import models

from members.models import Member
from posts.models import Post


# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    pub_date = models.DateTimeField('date published')