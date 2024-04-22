from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from app.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))


class SignUpForm(ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    confirm_password = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    nickname = forms.CharField(label='Nickname', widget=forms.TextInput(attrs={'placeholder': 'Enter your nickname'}))
    avatar = forms.ImageField(label='Avatar', required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords must match")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        profile = Profile.objects.create(user=user)
        profile.avatar = self.cleaned_data['avatar']
        profile.name = self.cleaned_data['nickname']
        profile.save()
        return user
