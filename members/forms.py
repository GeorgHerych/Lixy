from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from members.models import LoginMember, ResetPassword, Member, Country, City


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

    class Meta:
        model = Member
        fields = ('banner', 'avatar', 'username', 'first_name', 'last_name', 'gender', 'birthdate', 'country', 'city', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        selected_country = kwargs.get('country', None)
        selected_city = kwargs.get('city', None)

        self.fields['city'].queryset = City.objects.all()

        if selected_city:
            self.fields['city'].initial = selected_city

        print(selected_city)
        print(self.fields['city'].initial)

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