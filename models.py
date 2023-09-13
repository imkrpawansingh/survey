# survey_app/models.py

from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=255)

class Question(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

class Response(models.Model):
    candidate_name = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.IntegerField(null=True, blank=True)



# Create your models here.
