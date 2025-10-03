from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from comments.forms import CreateCommentForm, EditCommentForm
from comments.models import Comment
from posts.helpers.localtimemanager import set_local_time_to_models, set_local_time_to_model
from posts.models import Post


# Create your views here.
@login_required(login_url="/members/login")
def comments(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_list = Comment.objects.filter(post_id=post_id)

    set_local_time_to_model(post, 'pub_date')

    ordered_comments = comment_list.order_by('-pub_date')
    set_local_time_to_models(ordered_comments, 'pub_date')

    form = CreateCommentForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            form.save(user=request.user, post=post)

            comment_list = Comment.objects.filter(post_id=post_id)
            ordered_comments = comment_list.order_by('-pub_date')
            set_local_time_to_models(ordered_comments, 'pub_date')

    form = CreateCommentForm()

    return render(request, "comments/comments.html", {"post": post, "comments": ordered_comments, "form": form})

@login_required(login_url="/members/login")
def edit_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)

    form = EditCommentForm(request.POST, instance=comment)

    if request.method == "POST":
        if form.is_valid():
            form.save()

        return redirect(f"/post/{post_id}/comments/")

    form = EditCommentForm(instance=comment)

    return render(request, "comments/edit_comment.html", {"form": form})

@login_required(login_url="/members/login")
def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    return redirect(f"/post/{post_id}/comments/")