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

    RELATIONSHIP_STATUSES = (
        ("single", "Сам/сама"),
        ("relationship", "У стосунках"),
        ("married", "Одружений/а"),
        ("complicated", "Все складно"),
        ("prefer_not", "Не вказувати"),
    )

    RELATIONSHIP_GOALS = (
        ("dating", "Побачення"),
        ("long_term", "Серйозні стосунки"),
        ("friendship", "Дружба"),
        ("networking", "Нетворкінг"),
        ("casual", "Неформальне спілкування"),
    )

    SEXUAL_ORIENTATIONS = (
        ("heterosexual", "Гетеро"),
        ("homosexual", "Гомо"),
        ("bisexual", "Бісексуал"),
        ("asexual", "Асекс"),
        ("questioning", "У пошуках себе"),
        ("prefer_not", "Не вказувати"),
    )

    BODY_TYPES = (
        ("slim", "Струнка"),
        ("average", "Середня"),
        ("athletic", "Атлетична"),
        ("curvy", "Пишна"),
        ("plus", "Plus size"),
    )

    EDUCATION_LEVELS = (
        ("secondary", "Середня освіта"),
        ("vocational", "Професійна освіта"),
        ("bachelor", "Бакалавр"),
        ("master", "Магістр"),
        ("phd", "PhD"),
        ("prefer_not", "Не вказувати"),
    )

    CHILDREN_PREFERENCES = (
        ("no", "Немає"),
        ("someday", "Можливо у майбутньому"),
        ("have_not_living", "Є, але не проживаємо разом"),
        ("have_living", "Є, живемо разом"),
        ("prefer_not", "Не вказувати"),
    )

    HABITS = (
        ("no", "Ніколи"),
        ("occasionally", "Іноді"),
        ("socially", "У компанії"),
        ("regularly", "Регулярно"),
        ("prefer_not", "Не вказувати"),
    )

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
    relationship_status = models.CharField(max_length=32, choices=RELATIONSHIP_STATUSES, null=True, blank=True)
    relationship_goal = models.CharField(max_length=32, choices=RELATIONSHIP_GOALS, null=True, blank=True)
    sexual_orientation = models.CharField(max_length=32, choices=SEXUAL_ORIENTATIONS, null=True, blank=True)
    height_cm = models.PositiveSmallIntegerField(null=True, blank=True)
    body_type = models.CharField(max_length=32, choices=BODY_TYPES, null=True, blank=True)
    education_level = models.CharField(max_length=32, choices=EDUCATION_LEVELS, null=True, blank=True)
    occupation = models.CharField(max_length=120, null=True, blank=True)
    company = models.CharField(max_length=120, null=True, blank=True)
    languages = models.CharField(max_length=255, null=True, blank=True)
    interests = models.TextField(null=True, blank=True)
    children = models.CharField(max_length=32, choices=CHILDREN_PREFERENCES, null=True, blank=True)
    smoking = models.CharField(max_length=32, choices=HABITS, null=True, blank=True)
    drinking = models.CharField(max_length=32, choices=HABITS, null=True, blank=True)
