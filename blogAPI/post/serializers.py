from rest_framework import serializers
from .models import PostModel

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields= [
            "id",
            "author",
            "title",
            "content",
            "create_at",
            "update_at",
        ]
        model= PostModel