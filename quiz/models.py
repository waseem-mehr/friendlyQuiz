from django.db import models
from django.contrib.auth.forms import User
# Create your models here.


class Quiz(models.Model):
    quiz_id = models.IntegerField()
    quiz_text = models.CharField(max_length=100)
    quiz_choice1 = models.CharField(max_length=100)
    quiz_choice2 = models.CharField(max_length=100)
    quiz_choice3 = models.CharField(max_length=100)
    quiz_choice4 = models.CharField(max_length=100)
    quiz_choice5 = models.CharField(max_length=100)

    def __str__(self):
        return self.quiz_text


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    ans = models.CharField(max_length=100)

    def __str__(self):
        return self.quiz.quiz_text+"..."+self.user.username


class Answer(models.Model):
    friend = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    ans = models.CharField(max_length=100)

    def __str__(self):
        return self.quiz.quiz_text+"..."+self.friend
