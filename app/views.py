import random

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.views.decorators.http import require_http_methods, require_POST
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET

from app.forms import LoginForm, SignUpForm
from app.models import *

# Create your views here.
BEST_MEMBERS = Profile.objects.order_by('-rating')[:5]

colors = ['primary', 'secondary', 'danger', 'warning', 'info', 'dark']
POPULAR_TAGS = Tag.objects.annotate(count=Count('id')).order_by('-count')[:10]
for tag in POPULAR_TAGS:
    tag.color = random.choice(colors)


def paginate(object_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(object_list, per_page)
    try:
        page_obj = paginator.page(page_num)
        until_last = page_obj.paginator.num_pages - page_obj.number
    except PageNotAnInteger:
        return Http404()
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        until_last = 0
    return page_obj, until_last


@require_GET
def index(request):
    questions = Question.objects.get_new()
    page_obj, until_last = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {'questions': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})


@require_GET
def hot(request):
    questions = Question.objects.get_hot()
    page_obj, until_last = paginate(questions, request, 20)
    return render(request, 'hot.html',
                  {'questions': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})


@require_GET
@login_required(login_url='login')
def settings(request):
    return render(request, 'settings.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


@require_GET
@login_required(login_url='login')
def ask(request):
    return render(request, 'ask.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


@require_GET
def question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answers = Answer.object.get_answers(question)

    page_obj, until_last = paginate(answers, request, 30)
    return render(request, 'question.html',
                  {'question': question,
                   'answers': page_obj,
                   'members': BEST_MEMBERS,
                   'popular_tags': POPULAR_TAGS,
                   'until_last': until_last
                   })


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect('index')
            else:
                login_form.add_error(None, 'Wrong login or password!')

    return render(request, 'login.html', {
        'members': BEST_MEMBERS,
        'popular_tags': POPULAR_TAGS,
        'form': login_form,
    })


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        signup_form = SignUpForm()
    if request.method == 'POST':
        signup_form = SignUpForm(data=request.POST)
        if signup_form.is_valid():
            if User.objects.filter(username=signup_form.cleaned_data['username']).exists():
                signup_form.add_error('username', 'Login taken enter another and try again')
            elif User.objects.filter(email=signup_form.cleaned_data['email']).exists():
                signup_form.add_error('email', 'Email taken enter another and try again')
            else:
                user = signup_form.save()
                if user:
                    return redirect(reverse('login'))
                else:
                    signup_form.add_error(None, "User saving error!")

    return render(request, 'signup.html', {
        'members': BEST_MEMBERS,
        'popular_tags': POPULAR_TAGS,
        'form': signup_form,
    })


@require_GET
def tag(request, tag):
    try:
        questions = Question.objects.get_by_tag(tag)
    except ObjectDoesNotExist:
        raise Http404
    page_obj, until_last = paginate(questions, request, 20)
    return render(request, 'tag.html', {
        'tag': tag,
        'questions': page_obj,
        'members': BEST_MEMBERS,
        'popular_tags': POPULAR_TAGS,
        'until_last': until_last
    })
