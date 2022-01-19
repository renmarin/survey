from .models import Question, Option
from .serializers import QuestionSerializer, OptionSerializer, UserSerializer
from django.http import Http404
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .permissions import IsAuthorOrReadOnly

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .tasks import sent_email_to_admin


properties = {
    "text": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Text of the question",
        default="question[num]",
    ),
    "description": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="some additional description",
        default="description",
    ),
}


class QuestionsList(APIView):
    """
    List all Questions, or create a new Questions.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties)
    )
    def post(self, request, format=None):
        request.data['author'] = request.user.id
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # send email to admin (admarin) when creating a new question
            sent_email_to_admin.delay(
                "INFO",
                f"New Question: \"{request.data.get('text')}\" is created by {request.user} user",
                "server@example.com",
                ["admarin@example.com"],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    """
    Retrieve, update or delete a Questions instance.
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties=properties)
    )
    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        request.data['author'] = request.user.id
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
    "text": openapi.Schema(
        type=openapi.TYPE_STRING,
        description="Text of the question",
        default="question[num]",
    )
}


class OptionsList(APIView):
    """
    List all Options, or create a new Options.
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk, format=None):
        options = Option.objects.filter(question_id=pk).all()
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, properties=option_properties
        )
    )
    def post(self, request, pk, format=None):
        request.data['author'] = request.user.id
        question = Question.objects.get(pk=pk)
        # use entered option id when create option or current question id of none
        request.data['question'] = request.data.get('question', question.id)
        serializer = OptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sent_email_to_admin.delay(
                "INFO",
                f"New Option: \"{request.data.get('text')}\" is created by {request.user} user",
                "server@example.com",
                ["admarin@example.com"],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OptionDetail(APIView):
    """
    Retrieve, update or delete a Options instance.
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]

    def get_object(self, question_pk, option_pk):
        try:
            return Option.objects.filter(question_id=question_pk).get(pk=option_pk)
        except Option.DoesNotExist:
            raise Http404

    def get(self, request, question_pk, option_pk, format=None):
        option = self.get_object(question_pk, option_pk)
        serializer = OptionSerializer(option)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT, properties=option_properties
        )
    )
    def put(self, request, question_pk, option_pk, format=None):
        question = Question.objects.get(pk=question_pk)
        # use entered option id when create option or current question id of none
        request.data['question'] = request.data.get('question', question.id)
        request.data['author'] = request.user.id
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


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
