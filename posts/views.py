from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from posts.helpers.localtimemanager import set_local_time_to_models, set_local_time_to_model
from posts.forms import CreatePostForm, EditPostForm
from posts.helpers.prevpagesession import set_prev_page, get_prev_page
from posts.models import Post, PostAttachment, SavedPost, HiddenPost


# Create your views here.

@login_required(login_url="/members/login")
def posts(request):
    set_prev_page(request.session, "")
    post_list = Post.objects.all()
    member = request.user
    saved_post_list = SavedPost.objects.filter(member=member)
    saved_posts_ids = saved_post_list.values_list('post__id', flat=True)
    hidden_post_list = HiddenPost.objects.filter(member=member)
    hidden_posts_ids = hidden_post_list.values_list('post__id', flat=True)

    form = create_post(request, '/')

    ordered_posts = post_list.order_by('-pub_date')
    set_local_time_to_models(ordered_posts, 'pub_date')

    return render(request, 'posts/posts.html', { 'form': form, 'posts': ordered_posts, 'saved_post_ids': saved_posts_ids, 'hidden_post_ids': hidden_posts_ids })

@login_required(login_url="/members/login")
def following_posts(request):
    set_prev_page(request.session, "")
    member = request.user
    following_members = member.followings.all()
    post_list = Post.objects.filter(member__in=following_members).order_by('-pub_date')
    saved_post_list = SavedPost.objects.filter(member=member)
    saved_posts_ids = saved_post_list.values_list('post__id', flat=True)
    hidden_post_list = HiddenPost.objects.filter(member=member)
    hidden_posts_ids = hidden_post_list.values_list('post__id', flat=True)

    form = create_post(request, '/')

    ordered_posts = post_list.order_by('-pub_date')
    set_local_time_to_models(ordered_posts, 'pub_date')

    return render(request, 'posts/posts.html', { 'form': form, 'posts': ordered_posts, 'saved_post_ids': saved_posts_ids, 'hidden_post_ids': hidden_posts_ids })

@login_required(login_url="/members/login")
def create_post(request, redirect_url):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, request.user)

        if form.is_valid():
            post = form.save(user=request.user, commit=False)
            post.save()

            images = request.FILES.getlist('image')
            videos = request.FILES.getlist('video')

            for image in images:
                PostAttachment.objects.create(post=post, attachment=image, type="image")

            for video in videos:
                PostAttachment.objects.create(post=post, attachment=video, type="video")

            return form

    return CreatePostForm()

@login_required(login_url="/members/login")
def delete_post(request, post_id):
    previous_url = get_prev_page(request.session)

    post = Post.objects.get(id=post_id)

    post.delete()


    return redirect(previous_url)

@login_required(login_url="/members/login")
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    previous_url = get_prev_page(request.session)

    if request.method == "POST":
        form = EditPostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()

            images = request.FILES.getlist('image')
            videos = request.FILES.getlist('video')

            for image in images:
                PostAttachment.objects.create(post=post, attachment=image, type="image")

            for video in videos:
                PostAttachment.objects.create(post=post, attachment=video, type="video")

            return redirect(previous_url)

    form = EditPostForm(instance=post)

    return render(request, 'posts/edit_post_form.html', {'form': form})

@login_required(login_url="/members/login")
def delete_attachment(request, post_id, attachment_id):
    attachment = PostAttachment.objects.get(id=attachment_id)

    attachment.attachment.delete()
    attachment.delete()

    return redirect(f"/posts/edit-post/{post_id}")

@login_required(login_url="/members/login")
def saved_posts(request):
    set_prev_page(request.session, "/posts/saved-posts")
    member = request.user
    saved_post_list = SavedPost.objects.filter(member=member)

    for saved_post in saved_post_list:
        set_local_time_to_model(saved_post.post, "pub_date")

    saved_posts_ids = saved_post_list.values_list('post__id', flat=True)

    hidden_post_list = HiddenPost.objects.filter(member=member)
    hidden_posts_ids = hidden_post_list.values_list('post__id', flat=True)

    return render(request, 'posts/saved_posts.html', { 'posts': saved_post_list, 'saved_post_ids': saved_posts_ids, 'hidden_post_ids': hidden_posts_ids })

@login_required(login_url="/members/login")
def hide_post(request, post_id):
    prev_page = get_prev_page(request.session)
    post = Post.objects.get(id=post_id)
    member = request.user

    if post not in member.hidden_posts.all():
        HiddenPost.objects.create(member=member, post=post)

    return redirect(prev_page)

@login_required(login_url="/members/login")
def save_post(request, post_id):
    prev_page = get_prev_page(request.session)
    post = Post.objects.get(id=post_id)
    member = request.user

    if post not in member.saved_posts.all():
        SavedPost.objects.create(member=member, post=post)

    return redirect(prev_page)

@login_required(login_url="/members/login")
def unsave_post(request, post_id):
    prev_page = get_prev_page(request.session)
    post = Post.objects.get(id=post_id)
    member = request.user
    saved_posts_ids = member.saved_posts.all().values_list('post__id', flat=True)

    if post.id in saved_posts_ids:
        SavedPost.objects.filter(member=member, post=post).delete()

    return redirect(prev_page)