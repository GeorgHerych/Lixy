from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class LoginMember(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class ResetPassword(models.Model):
    username = models.CharField(max_length=20)
    new_password = models.CharField(max_length=20)
    new_password2 = models.CharField(max_length=20)

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name

class Member(AbstractUser):
    Genders = {
        "M": "Male",
        "F": "Female"
    }

    banner = models.ImageField(upload_to='bgs/', null=True, blank=True, default='/bgs/default/default_banner.png')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='/avatars/default/default_avatar_light.png')
    gender = models.CharField(max_length=20, null=True, blank=True, choices=Genders.items())
    birthdate = models.DateField(null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    privacy_settings = models.BooleanField(default=False)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings', blank=True)
