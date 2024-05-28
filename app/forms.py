from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

from app.models import Profile, Question, Tag, Answer


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


class AskForm(forms.ModelForm):
    tags = forms.CharField(label='Tags', max_length=100,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter tags separated by commas'}))
    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

    def clean_tags(self):
        tags = self.cleaned_data.get("tags")
        cleaned_tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
        return cleaned_tags
    def save(self, user=None, commit=True):
        question = super().save(commit=False)
        if user:
            question.user = user
        question.save()
        tags = self.cleaned_data['tags']
        tags_set = []
        for tag_name in tags:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags_set.append(tag.id if tag else None)
        question.tags.set(tags_set)
        return question

class AnswerForm(forms.ModelForm):
    content = forms.CharField(label='Answer',widget=forms.Textarea(attrs={ 'placeholder': 'Enter your answer'}))

    class Meta:
        model = Answer
        fields = ['content']

    def save(self, question=None, user=None, commit=True):
        answer = super().save(commit=False)
        if question and user:
            answer.question = question
            answer.user = user
            answer.save()
        return answer