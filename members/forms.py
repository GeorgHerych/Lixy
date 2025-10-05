from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from members.models import LoginMember, ResetPassword, Member, Country, City, DialogMessage


# class BaseMemberCreationForm(BaseUserCreationForm):
#     class Meta(BaseUserCreationForm.Meta):
#         model = Member
#
# class MemberCreationForm(BaseMemberCreationForm, UserCreationForm):
#     pass

class RegisterUserForm(UserCreationForm):
    # avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}), required=False, label='')
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), label='')
    first_name = forms.CharField(max_length=50 , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), label='')
    last_name = forms.CharField(max_length=50 , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), label='')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), label='')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}), label='')

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class LoginUserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}), label='')

    class Meta:
        model = LoginMember
        fields = ('username', 'password')

class ResetPasswordForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), label='')
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}), label='')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat New Password'}), label='')

    class Meta:
        model = ResetPassword
        fields = ('username', 'new_password', 'new_password2')

class EditMemberForm(forms.ModelForm):
    banner = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control hidden', 'id': 'id_banner'}), label='')
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control hidden', 'id': 'id_avatar'}), label='')
    username = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}), label='')
    first_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), label='')
    last_name = forms.CharField(required=False, max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), label='')
    gender = forms.ChoiceField(required=False, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Gender'}), choices=Member.Genders, label='')
    birthdate = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Birthdate', 'type': 'date'}), label='')
    country = forms.ModelChoiceField(required=False, queryset=Country.objects.all(), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}), label='')
    city = forms.ModelChoiceField(required=False, queryset=City.objects.none(), widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'City'}), label='')
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Tell about yourself'}), label='')
    relationship_status = forms.ChoiceField(
        required=False,
        choices=[('', 'Сімейний стан')] + list(Member.RELATIONSHIP_STATUSES),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )
    relationship_goal = forms.ChoiceField(
        required=False,
        choices=[('', 'Мета знайомства')] + list(Member.RELATIONSHIP_GOALS),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )
    sexual_orientation = forms.ChoiceField(
        required=False,
        choices=[('', 'Сексуальна орієнтація')] + list(Member.SEXUAL_ORIENTATIONS),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )
    height_cm = forms.IntegerField(
        required=False,
        min_value=100,
        max_value=250,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Зріст (см)'}),
        label=''
    )
    body_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Тип статури')] + list(Member.BODY_TYPES),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )
    education_level = forms.ChoiceField(
        required=False,
        choices=[('', 'Освіта')] + list(Member.EDUCATION_LEVELS),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )
    occupation = forms.CharField(
        required=False,
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Професія'}),
        label=''
    )
    company = forms.CharField(
        required=False,
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Місце роботи'}),
        label=''
    )
    languages = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Мови, якими спілкуєтеся'}),
        label=''
    )
    interests = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Хобі та інтереси'}),
        label=''
    )
    children = forms.ChoiceField(
        required=False,
        choices=[('', 'Діти')] + list(Member.CHILDREN_PREFERENCES),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )
    smoking = forms.ChoiceField(
        required=False,
        choices=[('', 'Ставлення до куріння')] + list(Member.HABITS),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )
    drinking = forms.ChoiceField(
        required=False,
        choices=[('', 'Ставлення до алкоголю')] + list(Member.HABITS),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label=''
    )

    class Meta:
        model = Member
        fields = (
            'banner',
            'avatar',
            'username',
            'first_name',
            'last_name',
            'gender',
            'birthdate',
            'country',
            'city',
            'bio',
            'relationship_status',
            'relationship_goal',
            'sexual_orientation',
            'height_cm',
            'body_type',
            'education_level',
            'occupation',
            'company',
            'languages',
            'interests',
            'children',
            'smoking',
            'drinking',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['city'].queryset = City.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get('country')
        city = cleaned_data.get('city')

        if country and city:
            if not City.objects.filter(name=city, country=country).exists():
                raise forms.ValidationError("The selected city does not belong to the selected country.")

        return cleaned_data

    # def save(self, commit=True):
    #     member = super().save(commit=False)
    #
    #     print(member.country)
    #
    #     if member.country == None:
    #         member.country = Country.objects.all()[0]
    #
    #     if member.city == None:
    #         member.city = City.objects.all()[0]
    #
    #     if commit:
    #         member.save()
    #
    #     return member


class DialogMessageForm(forms.ModelForm):
    text = forms.CharField(
        label="",
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Напишіть повідомлення…",
                "autocomplete": "off",
            }
        ),
    )

    class Meta:
        model = DialogMessage
        fields = ("text",)

    def clean_text(self):
        text = self.cleaned_data.get("text", "")
        text = text.strip()
        if not text:
            raise forms.ValidationError("Повідомлення не може бути порожнім.")
        return text
