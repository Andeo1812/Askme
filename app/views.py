from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from app.models import *
from app.forms import *
import paginator
from Askme.settings import REDIRECT_FIELD_NAME

users = Profile.objects.get_top_users(count=6)

top_tags = Tag.objects.top_tags(count=6)

def index(request):
    questions = Question.objects.new()
    content = paginator.paginate(questions, request, 10)
    content.update({"category": "New questions",
                    "forward_category": "Best questions",
                    'best_members': users,
                    "key": "authorized",
                    "popular_tags": top_tags})

    return render(request, "index.html", content)


def hot(request):
    questions = Question.objects.hot()
    content = paginator.paginate(questions, request, 10)
    content.update({
        "category": "Best questions",
        "forward_category": "New question",
        "popular_tags": top_tags,
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
                                                  "popular_tags": top_tags,
                                                  'best_members': users
                                                  })

    content = paginator.paginate(answers, request, 3)
    content.update({'question': question,
                    'popular_tags': top_tags,
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
                                                  "popular_tags": top_tags,
                                                  'best_members': users
                                                  })
    content = paginator.paginate(tags, request, 3)
    content.update(
        {'best_members': users,
         'popular_tags': top_tags,
         "one_tag": tag})

    return render(request, "tag.html", content)

@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
def ask(request):
    if request.method == "GET":
        form = AskForm()
    elif request.method == 'POST':
        form = AskForm(data=request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = Profile.objects.get(user=request.user)
            question.save()
            for tag in form.cleaned_data['tag_list'].split():
                new = Tag.objects.get_or_create(name=tag)[0]
                question.tags.add(new)
            question.save()
            return redirect("one_question", question_id=question.id)
        form.save()

    return render(request, 'ask.html', {'form': form, 'popular_tags': top_tags, 'best_members': users, "key": "authorized"})


def login(request):
    if request.method == 'GET':
        user_form = LoginForm()
    elif request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request, **user_form.cleaned_data)
            if user:
                return redirect(reverse("new"))
            user_form.add_error('password', "Not such Login/Password")

    return render(request, 'login.html', {'form': user_form, 'popular_tags': top_tags, 'best_members': users})


@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
def logout_view(request):
    auth.logout(request)
    prev = cache.get(REDIRECT_FIELD_NAME)
    if not prev:
        prev = "new"
    cache.delete(REDIRECT_FIELD_NAME)
    return redirect(prev)


def signup(request):
    if request.method == 'GET':
        user_form = RegisterForm()
    elif request.method == 'POST':
        user_form = RegisterForm(data=request.POST)
        if user_form.is_valid():
            form_data = user_form.cleaned_data.pop("password_repeat")
            form_avatar = user_form.cleaned_data.pop("avatar")
            user = User.objects.create_user(**user_form.cleaned_data)
            user.save()
            Profile.objects.create(user=user, avatar=form_avatar)
            return redirect("new")
        user_form.add_error('password', "User exist")

    return render(request, 'signup.html', {'form': user_form, 'popular_tags': top_tags, 'best_members': users})


def user_settings(request):
    return render(request, 'user_settings.html', {"key": "authorized", 'popular_tags': top_tags, 'best_members': users})


