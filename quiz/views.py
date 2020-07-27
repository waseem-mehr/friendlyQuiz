from django.shortcuts import render, redirect
from .forms import SignupForm
from django.http import HttpResponse
from django.contrib import messages
from .models import Question, Answer, Quiz
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/login")
def home(request):
    user = User.objects.get(username=request.user)
    question = Question.objects.filter(user=user).first()
    create = False
    if question:
        create = True
    context = {
        "create": create
    }
    return render(request, 'quiz/home.html', context)


@login_required(login_url="/login")
def quiz(request, id):
    if request.method == 'POST':
        if "answer" in request.POST:
            answer = request.POST.get('answer')
            quiz_id = id-1
            quiz = Quiz.objects.all()
            quiz = quiz.get(quiz_id=quiz_id)
            user = User.objects.get(username=request.user)
            question = Question.objects.create(
                user=user,
                quiz=quiz,
                ans=answer,
            )

        if id <= 10:
            quiz = Quiz.objects.all()
            quiz = quiz.get(quiz_id=id)
            context = {
                "quiz": quiz,
                "id": id+1,
                "user": request.user
            }
            return render(request, 'quiz/quizes.html', context)
        else:
            return redirect('/quiz/submit/')


@login_required(login_url="/login")
def quizSubmit(request):
    user = request.user
    urlofquiz = f"https://friendlyquiz.herokuapp.com/attemptQuiz/{user}"
    context = {
        "urlofquiz": urlofquiz
    }
    return render(request, 'quiz/submit.html', context)


def results(request):
    if request.user.is_authenticated:
        user = request.user
        auth = True
    else:
        user = request.GET.get('user')
        auth = False
    urlofquiz = f"https://friendlyquiz.herokuapp.com/attemptQuiz/{user}"
    friends = set()
    userobj = User.objects.get(username=user)
    questions = Question.objects.filter(user=userobj)
    answers = Answer.objects.filter(user=userobj)
    for answer in answers:
        friends.add(answer.friend)
    scores = []
    for friend in friends:
        score = 0
        for x in range(1, 10):
            quiz = Quiz.objects.get(quiz_id=x)
            q = questions.filter(quiz=quiz)
            ans = answers.filter(friend=friend)
            ans = ans.filter(quiz=quiz)
            for f, b in zip(q, ans):
                if f.ans == b.ans:
                    score = score+1

        f = {
            "friend": friend,
            "score": (score/10)*100
        }
        scores.append(f)
   
    context = {
        "urlofquiz": urlofquiz,
        "scores": scores

    }
    return render(request, 'quiz/results.html', context)


@login_required(login_url='/login')
def createdQuizes(request):
    user = User.objects.get(username=request.user)
    questions = Question.objects.filter(user=user)
    context = {
        "questions": questions,
    }
    return render(request, 'quiz/createdQuizes.html', context)


def attemptQuiz(request, useris):
    context = {
        "user": useris
    }
    return render(request, 'quiz/attemptQuiz.html', context)


def attempt(request, useris, id):
    if request.method == "GET":
        if "friend" in request.GET:
            friend = request.GET.get('friend')
            quiz = Quiz.objects.get(quiz_id=id)
            context = {
                "quiz": quiz,
                "id": id,
                "friend": friend,
                "user": useris
            }
            return render(request, 'quiz/attempt.html', context)
    if request.method == "POST":
        if id <= 10:
            friend = request.GET.get('friend')
            quiz = Quiz.objects.get(quiz_id=id)
            user = User.objects.get(username=useris)
            answer = request.POST.get('answer')
            answer = Answer.objects.create(
                friend=friend,
                user=user,
                quiz=quiz,
                ans=answer
            )
            if id+1 <= 10:
                quiz = Quiz.objects.get(quiz_id=id+1)
                context = {
                    "quiz": quiz,
                    "id": id+1,
                    "friend": friend,
                    "user": useris
                }
                return render(request, 'quiz/attempt.html', context)
            else:
                return redirect('/results/?user='+useris)
        else:
            return redirect('/results/?user='+useris)


def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        if "login" in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.warning(request, 'Username Or Password not matched.')
                return redirect('/login')
    context = {}
    return render(request, 'quiz/login.html', context)


def signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        if "signup" in request.POST:
            user = SignupForm(request.POST)
            if user.is_valid():
                user.save()
                return redirect('/login')
            else:
                context = {
                    "errors": user.errors
                }
                return render(request, 'quiz/signup.html', context)
    context = {
        "form": SignupForm()
    }   
    return render(request, 'quiz/signup.html', context)


def logoutView(request):
    logout(request)
    return redirect('/login')
