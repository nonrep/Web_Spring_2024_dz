import random
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render

from app.models import *

# Create your views here.
BEST_MEMBERS = Profile.objects.order_by('-rating')[:5]

colors = ['primary', 'secondary', 'danger', 'warning', 'info', 'light', 'dark']
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


def index(request):
    questions = Question.objects.get_new()
    page_obj, until_last = paginate(questions, request, 20)
    return render(request, 'index.html',
                  {'questions': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})


def hot(request):
    try:
        questions = Question.objects.get_hot()
    except Question.DoesNotExist:
        return Http404('Questions does not exist')
    page_obj, until_last = paginate(questions, request, 20)
    return render(request, 'hot.html',
                  {'questions': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})


def settings(request):
    return render(request, 'settings.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


def ask(request):
    return render(request, 'ask.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


def question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
        answers = Answer.object.get_answers(question)
    except IndexError:
        raise Http404('Question not found')
    page_obj, until_last = paginate(answers, request, 30)
    return render(request, 'question.html',
                  {'question': question, 'answers': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})


def login(request):
    return render(request, 'login.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


def signup(request):
    return render(request, 'signup.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


def tag(request, tag):
    try:
        questions = Question.objects.get_by_tag(tag)
    except IndexError:
        raise Http404('Tag not found')
    page_obj, until_last = paginate(questions, request, 20)
    return render(request, 'tag.html',
                  {'tag': tag, 'questions': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})
