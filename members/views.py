from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count

from members.forms import RegisterUserForm, LoginUserForm, ResetPasswordForm, EditMemberForm
from members.models import Member, Country, City
from posts.helpers.passwordvalidator import is_password_valid
from posts.helpers.prevpagesession import set_prev_page


# Create your views here.
def login_user(request):
    form = LoginUserForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        username:str = form.cleaned_data['username']
        password:str = form.cleaned_data['password']

        member:Member|None = authenticate(request, username=username, password=password)

        if member is not None:
            login(request, member)

            return redirect('/')
        else:
            messages.error(request, "Your email or password is incorrect.")

            return redirect('login')

    form = LoginUserForm()

    return render(request, 'authenticate/login.html', {'form': form})

def logout_user(request):
    logout(request)

    return redirect('/')

def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            member = authenticate(username=username, password=password)
            login(request, member)

            messages.success(request, "Registration Successful.")

            return redirect('/')

    form = RegisterUserForm()

    return render(request, 'authenticate/register.html', {'form': form})

def reset_password(request):
    form = ResetPasswordForm(request.POST)

    if request.method == 'POST' and form.is_valid():

        username:str = form.cleaned_data['username']
        new_password:str = form.cleaned_data['new_password']
        new_password2:str = form.cleaned_data['new_password2']

        member:Member = None

        try:
            member = Member.objects.get(username=username)
        except Member.DoesNotExist:
            messages.error(request, f"User with username '{username}' doesn't exist.")

        if new_password == new_password2:
            is_valid = is_password_valid(new_password)

            if is_valid:
                member.set_password(new_password)
                member.save()

                messages.success(request, "Password changed successfully.")

                return redirect('/members/login')
            else:
                messages.error(request, "Password must contain digits, letters and special characters.")
        else:
            messages.error(request, f"Passwords don't match.")

    form = ResetPasswordForm()

    return render(request, 'authenticate/reset_password.html', {'form': form})

@login_required(login_url="/members/login")
def profile(request, username):
    set_prev_page(request.session, f"/members/profile/{username}")
    member = Member.objects.get(username=username)
    member_age = _calculate_age(member.birthdate)

    similar_members_qs = Member.objects.exclude(id=member.id)

    if member.country_id:
        similar_members_qs = similar_members_qs.filter(country=member.country)

    if member.city_id:
        similar_members_qs = similar_members_qs.filter(city=member.city)

    if member.gender:
        similar_members_qs = similar_members_qs.filter(gender=member.gender)

    similar_members = []

    for similar_member in similar_members_qs.select_related('country', 'city')[:5]:
        similar_members.append({
            'username': similar_member.username,
            'name': similar_member.get_full_name() or similar_member.username,
            'age': _calculate_age(similar_member.birthdate),
            'city': similar_member.city.name if similar_member.city else "",
            'country': similar_member.country.name if similar_member.country else "",
            'avatar': similar_member.avatar.url if similar_member.avatar else "",
            'gender_display': similar_member.get_gender_display() if similar_member.gender else None,
        })

    top_liked_members = []

    top_liked_qs = (
        Member.objects.exclude(id=member.id)
        .annotate(followers_count=Count('followers'))
        .order_by('-followers_count', 'username')
    )

    for liked_member in top_liked_qs.select_related('country', 'city')[:5]:
        top_liked_members.append({
            'username': liked_member.username,
            'name': liked_member.get_full_name() or liked_member.username,
            'age': _calculate_age(liked_member.birthdate),
            'city': liked_member.city.name if liked_member.city else "",
            'country': liked_member.country.name if liked_member.country else "",
            'avatar': liked_member.avatar.url if liked_member.avatar else "",
            'gender_display': liked_member.get_gender_display() if liked_member.gender else None,
            'followers_count': liked_member.followers_count,
        })

    context = {
        'member': member,
        'member_age': member_age,
        'recommendations': {
            'similar': similar_members,
            'top_liked': top_liked_members,
        },
    }

    return render(request, 'profile/profile.html', context)


def _calculate_age(birthdate):
    if not birthdate:
        return None

    today = date.today()
    years = today.year - birthdate.year

    if (today.month, today.day) >= (birthdate.month, birthdate.day):
        return years

    return years - 1


@login_required(login_url="/members/login")
def discover(request):
    set_prev_page(request.session, "/members/discover/")

    members = Member.objects.exclude(id=request.user.id).select_related('country', 'city')

    member_cards = []

    for member in members:
        age = _calculate_age(member.birthdate)

        member_cards.append({
            'username': member.username,
            'name': member.get_full_name() or member.username,
            'gender': member.gender,
            'gender_display': member.get_gender_display() if member.gender else None,
            'age': age,
            'bio': member.bio or "",
            'city': member.city.name if member.city else "",
            'city_id': member.city.id if member.city else None,
            'country': member.country.name if member.country else "",
            'country_id': member.country.id if member.country else None,
            'avatar': member.avatar.url if member.avatar else "",
            'banner': member.banner.url if member.banner else "",
        })

    context = {
        'members_data': member_cards,
    }

    return render(request, 'profile/discover.html', context)


@login_required(login_url="/members/login")
def edit_profile(request, username):
    user = request.user
    member = Member.objects.get(username=username)
    country = None
    city = None

    if member.country:
        try:
            country = Country.objects.get(name=member.country)
        except Country.DoesNotExist:
            country = None

    if member.city:
        try:
            city = City.objects.get(name=member.city)
        except City.DoesNotExist:
            city = None


    if (user.is_authenticated and user.username == member.username):
        if request.method == 'POST':
            form = EditMemberForm(request.POST, request.FILES, instance=member, initial={'country': country, 'city':city})

            if form.is_valid():
                form.save()

                return redirect(f"/members/profile/{member.username}")
            else:
                print(form.errors)
    else:
        redirect('/login')

    form = EditMemberForm(instance=member, initial={'country': country, 'city': city})

    return render(request, 'profile/edit_profile.html', {'form': form, 'member': member})

@login_required(login_url="/members/login")
def delete_banner(request):
    user = request.user
    member = Member.objects.get(username=user.username)
    default_banner_url = "/bgs/default/default_banner.png"

    if member.banner and member.banner != default_banner_url:
        member.banner.delete()
        member.banner = default_banner_url

    member.save()

    return redirect(f"/members/profile/edit-profile/{user.username}", {'member': member})

@login_required(login_url="/members/login")
def delete_avatar(request):
    user = request.user
    member = Member.objects.get(username=user.username)
    default_avatars_url = "/avatars/default/default_avatar_light.png"

    if member.avatar and member.avatar != default_avatars_url:
        member.avatar.delete()
        member.avatar = default_avatars_url

    member.save()

    return redirect(f"/members/profile/edit-profile/{user.username}", {'member': member})

@login_required(login_url="/members/login")
def follow(request, username):
    user = request.user
    member = Member.objects.get(username=username)

    if (member not in user.followings.all()):
        user.followings.add(member)

    print(member.followers.all())
    print(member.followings.all())

    return redirect(f"/members/profile/{username}")

@login_required(login_url="/members/login")
def unfollow(request, username):
    user = request.user
    member = Member.objects.get(username=username)

    if (member in user.followings.all()):
        user.followings.remove(member)

    return redirect(f"/members/profile/{username}")

@login_required(login_url="/members/login")
def remove(request, username):
    user = request.user
    member = Member.objects.get(username=username)

    if (member in user.followers.all()):
        user.followers.remove(member)

    return redirect(f"/members/followers/{user.username}")

@login_required(login_url="/members/login")
def followings(request, username):
    member = Member.objects.get(username=username)
    followings = member.followings.all()

    return render(request, 'profile/followings/follower_followings.html', {'member': member, 'followers_followings': followings, 'type': 'followings', 'title_text': 'Followings'})

@login_required(login_url="/members/login")
def followers(request, username):
    member = Member.objects.get(username=username)
    followers = member.followers.all()

    return render(request, 'profile/followings/follower_followings.html', {'member': member, 'followers_followings': followers, 'type': 'followers', 'title_text': 'Followers'})

def get_cities(request):
    country_id = request.GET.get('country_id')

    if country_id:
        cities = City.objects.filter(country_id=country_id)
        cities_data = [{'id': city.pk, 'name': city.name} for city in cities]
        return JsonResponse(cities_data, safe=False)

    return JsonResponse([], safe=False)