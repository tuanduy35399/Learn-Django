from rest_framework import serializers
from app.models import Client, Post

    
class ClientV1Serializer(serializers.ModelSerializer):
    class Meta:
        model = Client     
        fields = ['id', 'name', 'gender', 'createdAt','lastAccess']
        extra_kwargs = {
            'id': {'read_only': True},
             #mấy tham số required và default ModelSerializer auto biết khỏi thêm cũng được
             #này viết cho biết
             # lưu ý: required và default không được phép cùng tồn tại hay khai báo chung 1 hàng
            'name': {'required': True},
            'gender': {'default': Client.Gender.MALE},
        }