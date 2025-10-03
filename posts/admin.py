from django.contrib import admin

from posts.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    search_fields = ('title',)
    list_filter = ('pub_date',)

# Register your models here.
admin.site.register(Post, PostAdmin)