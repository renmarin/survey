import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "survey.settings")

import django

django.setup()

from api_service.models import Question, Option
from django.contrib.auth.models import User


users = {f'user-{num}': f'user-{num}-password' for num in range(1, 11)}
questions = [f"Question-{num}" for num in range(1, 11)]
options = [f"Option-{num}" for num in range(1, 4)]


for index, (username, password) in enumerate(users.items()):
    user = User.objects.create_user(
        username=username,
        password=password,
    )
    user.save()
    question = Question(text=f"Question-{index+1}", description="description", author=user)
    question.save()
    for num in range(1, 4):
        option = Option(
            text=f"Option {question.id} - {num}",
            question=question,
            author=user,
        )
        option.save()
