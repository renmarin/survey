from django.db import models


class Question(models.Model):
    text = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Option(models.Model):
    text = models.CharField(max_length=200)
    question = models.ForeignKey(Question, related_name="options", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Meta(models.Model):
    day = models.CharField(max_length=50)
