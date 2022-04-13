from django.shortcuts import render
from app.models import *
import paginator

users = Profile.objects.get_top_users(count=10)

def index(request):
    questions = Question.objects.new()
    content = paginator.paginate(questions, request, 10)
    content.update({"category": "New questions",
                    "forward_category": "Best questions",
                    'best_members': users,
                    "key": "authorized",
                    "popular_tags": Tag.objects.top_tags()})

    return render(request, "index.html", content)


def hot(request):
    questions = Question.objects.hot()
    content = paginator.paginate(questions, request, 10)
    content.update({
        "category": "Best questions",
        "forward_category": "New question",
        "popular_tags": Tag.objects.top_tags(),
        "redirect_new": "new",
        'best_members': users})

    return render(request, 'index.html', content)


def question(request, question_id):
    try:
        question = Question.objects.get_by_id(question_id)
        answers = Answer.objects.answer_by_question(question_id)
    except Exception:
        return render(request, 'not_found.html', {"hot_page": "Best questions",
                                                  "new_page": "New questions",
                                                  "popular_tags": Tag.objects.top_tags(),
                                                  'best_members': users
                                                  })

    content = paginator.paginate(answers, request, 3)
    content.update({'question': question,
                    'popular_tags': Tag.objects.top_tags(),
                    'answers': paginator.paginate(answers, request, 3),
                    'best_members': users
                    })

    return render(request, "question_page.html", content)


def tag(request, tag):
    try:
        tags = Question.objects.by_tag(tag)
    except Exception:
        return render(request, 'not_found.html', {"hot_page": "Best questions",
                                                  "new_page": "New questions",
                                                  "popular_tags": Tag.objects.top_tags(),
                                                  'best_members': users
                                                  })
    content = paginator.paginate(tags, request, 3)
    content.update(
        {'best_members': users,
         'popular_tags': Tag.objects.top_tags(),
         "one_tag": tag})

    return render(request, "tag.html", content)


def ask(request):
    return render(request, 'ask.html', {'popular_tags': Tag.objects.top_tags(), 'best_members': users, "key": "authorized"})


def login(request):
    return render(request, 'login.html', {'popular_tags': Tag.objects.top_tags(), 'best_members': users})


def signup(request):
    return render(request, 'signup.html', {'popular_tags': Tag.objects.top_tags(), 'best_members': users})


def user_settings(request):
    return render(request, 'user_settings.html', {"key": "authorized", 'popular_tags': Tag.objects.top_tags(), 'best_members': users})


