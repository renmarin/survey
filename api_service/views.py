"""SWAGGER done poorly. Do not use {format} options, they are fake and no use.
PUT as update works fine. POST as create works fine.
(Not user friendly, better use DRF native interface)
DELETE options are perfectly fine"""

from .models import Question, Option
from .serializers import QuestionSerializer, OptionSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .tasks import sent_email_to_admin


properties = {
        'text': openapi.Schema(type=openapi.TYPE_STRING, description='Text of the question', default='question[num]'),
        'description': openapi.Schema(type=openapi.TYPE_STRING, description='some additional description',
                                      default='description'),
        'author': openapi.Schema(type=openapi.TYPE_STRING, description='author name', default='admarin'),
        'options': openapi.Schema(type=openapi.TYPE_OBJECT,
                                  description='options for question (not edible in question creation)'),
    }


class QuestionsList(APIView):
    """
    List all Questions, or create a new Questions.
    """
    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties))
    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # send email to admin (admarin) when creating a new question
            sent_email_to_admin.delay('INFO', "New Question Created", "server@example.com", ["admarin@example.com"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    """
    Retrieve, update or delete a Questions instance.
    """
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties))
    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        question = self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


option_properties = {
        'text': openapi.Schema(type=openapi.TYPE_STRING, description='Text of the question', default='question[num]'),
        'question': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of Question', default=1),
    }


class OptionsList(APIView):
    """
    List all Options, or create a new Options.
    """
    def get(self, request, pk, format=None):
        options = Option.objects.filter(question_id=pk).all()
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=option_properties))
    def post(self, request, pk, format=None):
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sent_email_to_admin.delay('INFO', "New Option Created", "server@example.com", ["admarin@example.com"])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OptionDetail(APIView):
    """
    Retrieve, update or delete a Options instance.
    """
    def get_object(self, question_pk, option_pk):
        try:
            return Option.objects.filter(question_id=question_pk).get(pk=option_pk)
        except Option.DoesNotExist:
            raise Http404

    def get(self, request, question_pk, option_pk, format=None):
        option = self.get_object(question_pk, option_pk)
        serializer = OptionSerializer(option)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=option_properties))
    def put(self, request, question_pk, option_pk, format=None):
        option = self.get_object(question_pk, option_pk)
        serializer = OptionSerializer(option, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, question_pk, option_pk, format=None):
        option = self.get_object(question_pk, option_pk)
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
