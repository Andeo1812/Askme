from django.shortcuts import render, redirect, reverse
from django.contrib import auth
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
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
        "forward_category": "New questions",
        "popular_tags": top_tags,
        "redirect_new": "new",
        'best_members': users})
    return render(request, 'index.html', content)


def question(request, question_id):
    cache.set(REDIRECT_FIELD_NAME, request.path)
    if request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            ans = form.save(commit=False)
            ans.author = Profile.objects.get(user=request.user)
            ans.question = Question.objects.get(id=question_id)
            ans.save()
            for tag in form.cleaned_data['tag_list'].split():
                new = Tag.objects.get_or_create(name=tag)[0]
                ans.tags.add(new)
            ans.save()
            return redirect("question", question_id=question_id)
    else:
        try:
            question = Question.objects.get_by_id(question_id)
            answers = Answer.objects.answer_by_question(question_id)
        except Exception:
            return render(request, 'not_found.html', {"hot_page": "Best questions",
                                                      "new_page": "New questions",
                                                      "popular_tags": top_tags,
                                                      'best_members': users
                                                      })
        else:
            form = AnswerForm()
            content = paginator.paginate(answers, request, 5)
            content.update({'question': question,
                            "one_question:": "yes",
                            'popular_tags': top_tags,
                            'answers': paginator.paginate(answers, request, 5),
                            'best_members': users,
                            "form": form
                            })
    return render(request, "question_page.html", content)


def tag(request, tag):
    content = {"hot_page": "Best questions",
               "new_page": "New questions",
               "popular_tags": top_tags,
               'best_members': users
               }
    try:
        tags = Question.objects.by_tag(tag)
    except Exception:
        return render(request, 'not_found.html', content)
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
            return redirect("question", question_id=question.id)
        form.save()

    return render(request, 'ask.html',
                  {'form': form, 'popular_tags': top_tags, 'best_members': users, "key": "authorized"})


def login(request):
    prev = cache.get(REDIRECT_FIELD_NAME)
    nxt = request.GET.get(REDIRECT_FIELD_NAME, prev)
    if not nxt:
        nxt = 'new'
    if request.user.is_authenticated:
        return redirect(nxt)

    if request.method == 'GET':
        user_form = LoginForm()
        cache.set(REDIRECT_FIELD_NAME, nxt)
    elif request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request, **user_form.cleaned_data)
            if user is not None:
                auth.login(request, user)
                next_url = cache.get(REDIRECT_FIELD_NAME)
                cache.delete(REDIRECT_FIELD_NAME)
                return redirect(next_url)
            user_form.add_error('password', "Not such Login/Password")
    from pprint import pformat
    print("\n\n", "-" * 100)
    print(f"HERE: {pformat(user_form)}")
    print("-" * 100, "\n\n")
    return render(request, 'login.html', {'form': user_form, 'popular_tags': top_tags, 'best_members': users})


@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
def logout_view(request):
    auth.logout(request)
    prev = cache.get(REDIRECT_FIELD_NAME)
    if not prev:
        prev = "new"
    cache.delete(REDIRECT_FIELD_NAME)
    return redirect(prev)


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'GET':
        user_form = RegisterForm()
    elif request.method == 'POST':
        user_form = RegisterForm(data=request.POST)
        if user_form.is_valid():
            form_data = user_form.cleaned_data.pop("password_repeat")
            user = User.objects.create_user(**user_form.cleaned_data)
            user.save()
            Profile.objects.create(user=user)
            auth.login(request, user)
            return redirect("new")
        user_form.add_error('password', "Wrong login/password")
    return render(request, 'signup.html', {'form': user_form, 'popular_tags': top_tags, 'best_members': users})


@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
@require_http_methods(["GET", "POST"])
def user_settings(request):
    if request.method == "GET":
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile_related.avatar
        form = SettingsForm(initial=initial_data)
    else:
        initial_data = request.POST
        instance = request.user
        form = SettingsForm(initial=initial_data, instance=instance, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("user_settings"))
    return render(request, 'user_settings.html', {"form": form, 'popular_tags': top_tags, 'best_members': users})


@login_required(login_url="login", redirect_field_name=REDIRECT_FIELD_NAME)
@require_POST
def like(request):
    question_id = request.POST['question_id']
    question = Question.objects.get(id=question_id)
    question.app_likes()
    return JsonResponse({'new_likes': question.get_likes()})

