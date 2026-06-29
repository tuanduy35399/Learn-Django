from rest_framework import serializers
from app.models import Post

class PostV1Serializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = ['id','author', 'title', 'content','createdAt', 'updateAt']
        