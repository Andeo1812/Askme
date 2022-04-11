from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
QUESTIONS = [
    {
        "title": f"Title #{i}",
        "text": f" This if text for question #{i}",
        "number": i,
    } for i in range(4)
]

def index(request):
    return render(request, "index.html", {"questions": QUESTIONS})


def ask(request):
    return render(request, "ask.html")


def question(request, i: int):
    return render(request, "question_page.html", {"question": QUESTIONS[i]})