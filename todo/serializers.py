from rest_framework import serializers
from django.utils import timezone
from .models import Task


class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()
    date_created = serializers.DateTimeField(default=timezone.now)
    date_end = serializers.DateTimeField(default=timezone.now().strftime("%d.%m.%Y %H:%M"))
    status = serializers.CharField(max_length=15, default="In progress")

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
