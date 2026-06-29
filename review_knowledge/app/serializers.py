from rest_framework import serializers
from .models import Client, Post

    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client     
        fields = ['id', 'name', 'gender', 'createdAt','lastAccess']
        extra_kwargs = {
            'id': {'read_only': True},
             #mấy tham số required và default ModelSerializer auto biết khỏi thêm cũng được
             #này viết cho biết
            'name': {'required': True},
            'gender': {'required': True, 'default': Client.Gender.MALE},
        }
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = ['id','author', 'title', 'content','createdAt', 'updateAt']

