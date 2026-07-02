from app.models import Client
from rest_framework import serializers

class ClientV2Serializers(serializers.ModelSerializer):
    class Meta:
        model= Client,
        # fields = ['id','name','gender','activate', 'createdAt', 'lastAccess']
        fields = '__all__'
    