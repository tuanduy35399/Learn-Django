from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Client, Post
from .serializers import ClientV1Serializer


@api_view(['GET','POST']) # de cac method o day
def client_list(request): 
    if request.method == 'GET':
        clients= Client.objects.all() # lay het data cua client tu db
        #chuan hoa
        serializers = ClientV1Serializer(clients, many = True) #many báo với serializer là đây là 1 list obj 
        return Response(data= serializers.data, status=status.HTTP_200_OK) 
        #co the de data =serializers.data hoac serializers.data cung duoc
        #nhung phai de dung thu tu Response(data= , status, template,...)
    elif request.method == 'POST':
        serializers = ClientV1Serializer(data= request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status.HTTP_201_CREATED) 
        #truyen khong dat ten positional argument (lap luan vi tri)
        return Response(serializers.errors, status.HTTP_400_BAD_REQUEST)