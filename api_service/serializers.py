from rest_framework import serializers
from .models import Question, Option


class QuestionSerializer(serializers.ModelSerializer):

    options = serializers.SlugRelatedField(
        many=True,
        queryset=Option.objects.all(),
        slug_field='text'
    )

    class Meta:
        model = Question
        fields = ["id", "text", "description", "created", "modified", "author", "options"]

    def create(self, validated_data):
        question = Question(
            text=validated_data['text'],
            description=validated_data['description'],
            author=validated_data['author'],
        )
        question.save()
        return question

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.description = validated_data.get('description', instance.description)
        instance.author = validated_data.get('author', instance.author)
        instance.modified = validated_data.get('modified', instance.modified)
        instance.save()
        return instance


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"

    def create(self, validated_data):
        option = Option(
            text=validated_data['text'],
            question=validated_data['question'],
        )
        option.save()
        return option
