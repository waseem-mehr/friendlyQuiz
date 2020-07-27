
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('quiz/<int:id>/', views.quiz, name="quiz"),
    path('quiz/submit/', views.quizSubmit, name="quizSubmit"),
    path('results/', views.results, name="results"),
    path('createdQuizes/', views.createdQuizes, name="createdQuized"),
    path('attemptQuiz/<str:useris>/', views.attemptQuiz, name="attemptQuiz"),
    path("attemptQuiz/<str:useris>/quiz/<int:id>/",
         views.attempt, name="attempt"),
    path('login/', views.loginView, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/',views.logoutView,name="logout")
]
