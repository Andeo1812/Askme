from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
QUESTIONS = []
for i in range(10):
    QUESTIONS.append({
        "title": "title " + str(i),
        "id": i,
        "views": i * 2,
        "votes": i,
        "likes": i * 3,
        "dislikes": i,
        "answers": i * 2,
        "author": "test@mail.com",
        "text": "text" + str(i) + "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor "
                                  "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud"
                                  " exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
                                  "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore"
                                  " eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in"
                                  " culpa qui officia deserunt mollit anim id est laborum1.",
        "tag1": "Python",
        "tag2": "C++",
        "tag3": "JS"
    })

ANSWERS = []
ANSWERS.append({
    "title": "title " + str(i),
    "id": 32,
    "views": 123,
    "votes": 123,
    "likes": 2,
    "dislikes": 3,
    "author": "testanswer1@mail.com",
    "text": "DO IT!",
    "tag1": "Python",
    "tag2": "Patterns",
    "tag3": "IO"
})

ANSWERS.append({
    "title": "title " + str(i),
    "id": 2,
    "views": 2,
    "votes": 42,
    "likes": 100,
    "dislikes": 0,
    "author": "testanswer2@mail.com",
    "text": "Yes, this is the best place, do your best and in a year you will see an excellent result, you need to prepare hard every day.",
    "tag1": "Python",
    "tag2": "Patterns",
})

NAME_TAGS = {
    "1": "Python",
    "2": "C++",
    "3": "Qt",
    "4": "C#",
    "5": "JS",
    "6": "Go",
    "7": "C",
    "8": "Rust",
    "9": "1C",
    "10": "Rudy",
    "11": "Pascal",
    "12": "TypeScript"
}

MEMBERS = {
    "0": "Bogdan007",
    "1": "Avenger303",
    "2": "Bomonec373",
    "3": "MC_Gogozik#",
}


def index(request):
    return render(request, "index.html", {"questions": QUESTIONS, "tags": NAME_TAGS, "members": MEMBERS})


def ask(request):
    return render(request, "ask.html", {"questions": QUESTIONS, "tags": NAME_TAGS, "members": MEMBERS})


def hot(request):
    return render(request, 'index.html', {"questions": QUESTIONS, "tags": NAME_TAGS, "members": MEMBERS})


def question(request, i: int):
    return render(request, "question_page.html", {"question": QUESTIONS[i], "tags": NAME_TAGS, "members": MEMBERS, "answers": ANSWERS})


def login(request):
    return render(request, "login.html", {"questions": QUESTIONS, "tags": NAME_TAGS, "members": MEMBERS})


def signup(request):
    return render(request, "signup.html", {"questions": QUESTIONS, "tags": NAME_TAGS, "members": MEMBERS})


def user_settings(request):
    return render(request, "user_settings.html", {"questions": QUESTIONS, "tags": NAME_TAGS, "members": MEMBERS})


def tag(request, name: str):
    return render(request, "tag.html", {"questions": QUESTIONS, "tags": NAME_TAGS, "members": MEMBERS, "tag": name})


def page(request, i: int):
    return render(request, 'index.html', {"questions": QUESTIONS, "tags": NAME_TAGS, "members": MEMBERS})
