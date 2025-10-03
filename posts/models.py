from django.db import models

from members.models import Member
from posts.helpers.localtimemanager import set_local_time_to_model


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(null=True, blank=True)
    pub_date = models.DateTimeField('date published')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    def delete(self):
        for post_attachment in self.attachments.all():
            post_attachment.delete()

        super().delete()

class PostAttachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='attachments')
    attachment = models.FileField(upload_to='post_media/', blank=True, null=True)
    type = models.CharField(max_length=100)

    def delete(self):
        if "https://" not in str(self.attachment):
            self.attachment.delete()

        super().delete()

class SavedPost(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_by_members')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'post')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.member.username} saved {self.post.title}"

class HiddenPost(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='hidden_posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='hidden_by_members')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('member', 'post')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.member.username} hidden {self.post.title}"