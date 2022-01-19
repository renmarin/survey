from rest_framework import serializers
from .models import Question, Option
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Question.objects.all()
    )
    options = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Option.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "questions", "options"]


class QuestionSerializer(serializers.ModelSerializer):

    options = serializers.SlugRelatedField(
        many=True, queryset=Option.objects.all(), slug_field="text", required=False
    )
    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "description",
            "created",
            "modified",
            "author",
            "author_username",
            "options",
        ]

    def create(self, validated_data):
        question = Question(
            text=validated_data["text"],
            description=validated_data["description"],
            author=validated_data["author"],
        )
        question.save()
        return question

    def update(self, instance, validated_data):
        instance.text = validated_data.get("text", instance.text)
        instance.description = validated_data.get("description", instance.description)
        instance.author = validated_data.get("author", instance.author)
        instance.modified = validated_data.get("modified", instance.modified)
        instance.save()
        return instance


class OptionSerializer(serializers.ModelSerializer):

    author_username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Option
        fields = [
            "id",
            "text",
            "question",
            "created",
            "modified",
            "author",
            "author",
            "author_username",
        ]

    def create(self, validated_data):
        option = Option(
            text=validated_data["text"],
            question=validated_data["question"],
            author=validated_data["author"],
        )
        option.save()
        return option
