from app.models import Post
from rest_framework import serializers

class PostV2Serializers(serializers.ModelSerializer):
    class Meta:
        model= Post,
        # fields = ['id', 'author', 'title', 'content', 'createdAt', 'updatedAt']
        fields = '__all__'