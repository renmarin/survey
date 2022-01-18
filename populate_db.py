import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'survey.settings')

import django
django.setup()

from api_service.models import Question, Option

Questions = [f"Question_{num}" for num in range(1, 11)]
Options = [f"Option_{num}" for num in range(1, 4)]

for question_num in Questions:
    question = Question(
        text=question_num,
        description="description",
        author="admarin"
    )
    question.save()
    for question_num in Options:
        option = Option(
            text=question_num,
            question=question,
        )
        option.save()
