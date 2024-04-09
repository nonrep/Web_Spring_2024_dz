from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'This is text of question {i}',
        'tags': ['first', 'second', 'third', 'fourth', 'fifth']
        ,
        'likes': (i + 4) % 5,
        'answers': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        'count_of_answers': 10
    } for i in range(200)
]

ANSWERS = [
    {
        'id': i,
        'text': f'This is answer {i}',
        'correct': True,
        'likes': (i + 2) % 5,
    } for i in range(20)
]

BEST_MEMBERS = [
    {
        'id': i,
        'nickname': f'Best member {i}',
    } for i in range(5)
]

colors = ['primary', 'secondary', 'danger', 'warning', 'info', 'light', 'dark']

POPULAR_TAGS = [
    {
        'id': i,
        'name': f'tag_{i}',
        'color': colors[i % 7],
    } for i in range(10)
]


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
    page_obj, until_last = paginate(QUESTIONS, request)
    return render(request, 'index.html',
                  {'questions': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})


def hot(request):
    page_obj, until_last = paginate(QUESTIONS, request)
    return render(request, 'hot.html',
                  {'questions': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})


def settings(request):
    return render(request, 'settings.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


def ask(request):
    return render(request, 'ask.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


def question(request, question_id):
    try:
        question = QUESTIONS[question_id]
        answers = []
        for answer in question['answers']:
            answers.append(ANSWERS[answer])
    except IndexError:
        raise Http404('Question not found')
    page_obj, until_last = paginate(answers, request, 3)
    return render(request, 'question.html',
                  {'question': question, 'answers': page_obj, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS,
                   'until_last': until_last})


def login(request):
    return render(request, 'login.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


def signup(request):
    return render(request, 'signup.html', {'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})


def tag(request, tag_id):
    try:
        questions = []
        for question in QUESTIONS:
            if tag_id in question['tags']:
                questions.append(question)
    except IndexError:
        raise Http404('Tag not found')
    return render(request, 'tag.html',
                  {'tag': tag_id, 'questions': questions, 'members': BEST_MEMBERS, 'popular_tags': POPULAR_TAGS})
