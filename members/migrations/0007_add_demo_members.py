from datetime import date

from django.db import migrations


def create_demo_members(apps, schema_editor):
    Member = apps.get_model('members', 'Member')
    Country = apps.get_model('members', 'Country')
    City = apps.get_model('members', 'City')

    demo_members = [
        {
            'username': 'daryna',
            'password': 'lixy_demo123',
            'first_name': 'Дарина',
            'last_name': 'Мельник',
            'email': 'daryna@example.com',
            'gender': 'F',
            'birthdate': date(1998, 6, 12),
            'country': 'Україна',
            'city': 'Київ',
            'bio': 'Обожнюю сучасне мистецтво, каву без цукру і прогулянки на світанку.',
            'relationship_goal': 'long_term',
            'occupation': 'Дизайнерка інтер’єрів',
            'company': 'Studio Light',
            'languages': 'Українська, Англійська',
            'interests': 'Музеї, урбаністика, подорожі, кераміка',
            'sexual_orientation': 'heterosexual',
            'height_cm': 170,
            'education_level': 'master',
            'children': 'no',
            'smoking': 'no',
            'drinking': 'socially',
            'avatar': 'avatars/alex-suprun-ZHvM3XIOHoE-unsplash.jpg',
        },
        {
            'username': 'oleksii',
            'password': 'lixy_demo123',
            'first_name': 'Олексій',
            'last_name': 'Романюк',
            'email': 'oleksii@example.com',
            'gender': 'M',
            'birthdate': date(1994, 11, 3),
            'country': 'Україна',
            'city': 'Львів',
            'bio': 'Фронтенд-розробник, любитель гірських походів і настільних ігор.',
            'relationship_goal': 'friendship',
            'occupation': 'Фронтенд-розробник',
            'company': 'Bright Apps',
            'languages': 'Українська, Англійська, Польська',
            'interests': 'Походи, ретро-ігри, лекції, фотографія',
            'sexual_orientation': 'heterosexual',
            'height_cm': 185,
            'education_level': 'bachelor',
            'children': 'no',
            'smoking': 'occasionally',
            'drinking': 'occasionally',
            'avatar': 'avatars/sigmund-jzz_3jWMzHA-unsplash.jpg',
        },
        {
            'username': 'sofia',
            'password': 'lixy_demo123',
            'first_name': 'Софія',
            'last_name': 'Гринчук',
            'email': 'sofia@example.com',
            'gender': 'F',
            'birthdate': date(1991, 2, 27),
            'country': 'Україна',
            'city': 'Одеса',
            'bio': 'Працюю у сфері івент-менеджменту, організовую фестивалі та камерні вечері.',
            'relationship_goal': 'dating',
            'occupation': 'Івент-менеджерка',
            'company': 'Black Sea Events',
            'languages': 'Українська, Англійська, Іспанська',
            'interests': 'Кулінарія, йога, театр, вініл',
            'sexual_orientation': 'heterosexual',
            'height_cm': 167,
            'education_level': 'bachelor',
            'children': 'someday',
            'smoking': 'no',
            'drinking': 'socially',
            'avatar': 'avatars/christian-buehner-DItYlc26zVI-unsplash.jpg',
        },
        {
            'username': 'maksym',
            'password': 'lixy_demo123',
            'first_name': 'Максим',
            'last_name': 'Дрозд',
            'email': 'maksym@example.com',
            'gender': 'M',
            'birthdate': date(1990, 8, 19),
            'country': 'Україна',
            'city': 'Харків',
            'bio': 'Викладаю історію мистецтва, часто подорожую на пленери та документую їх.',
            'relationship_goal': 'networking',
            'occupation': 'Викладач історії мистецтва',
            'company': 'Kharkiv Art School',
            'languages': 'Українська, Англійська, Німецька',
            'interests': 'Акварель, класична музика, велосипед, подкасти',
            'sexual_orientation': 'heterosexual',
            'height_cm': 178,
            'education_level': 'phd',
            'children': 'have_not_living',
            'smoking': 'no',
            'drinking': 'occasionally',
            'avatar': 'avatars/photo_2025-01-19_15-10-53.jpg',
        },
    ]

    for member_data in demo_members:
        username = member_data['username']
        if Member.objects.filter(username=username).exists():
            continue

        data = member_data.copy()
        password = data.pop('password')
        country_name = data.pop('country', None)
        city_name = data.pop('city', None)
        avatar_path = data.pop('avatar', None)
        data.pop('username', None)

        country = None
        if country_name:
            country, _ = Country.objects.get_or_create(name=country_name)

        city = None
        if city_name:
            if country is None:
                country, _ = Country.objects.get_or_create(name='Україна')
            city, _ = City.objects.get_or_create(name=city_name, country=country)

        email = data.pop('email', '')
        first_name = data.pop('first_name', '')
        last_name = data.pop('last_name', '')

        member = Member.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        if country:
            member.country = country
        if city:
            member.city = city
        if avatar_path:
            member.avatar = avatar_path

        for field, value in data.items():
            if hasattr(member, field):
                setattr(member, field, value)

        member.save()


def remove_demo_members(apps, schema_editor):
    Member = apps.get_model('members', 'Member')
    Member.objects.filter(username__in=['daryna', 'oleksii', 'sofia', 'maksym']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0006_member_body_type_member_children_member_company_and_more'),
    ]

    operations = [
        migrations.RunPython(create_demo_members, remove_demo_members),
    ]
