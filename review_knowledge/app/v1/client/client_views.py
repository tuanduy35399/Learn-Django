from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import Client
from .client_serializers import ClientV1Serializer


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
@api_view(['GET', 'PUT', 'DELETE'])
def client_detail(request, primary_key):
    #kiem tra su ton tai cua user
    try:
        client = Client.objects.get(pk = primary_key)
    except Client.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)\
    
    if request.method == 'GET':
        serializers = ClientV1Serializer(client)
        return Response(serializers.data, status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializers = ClientV1Serializer(client, data = request.data) 
        if serializers.is_valid(): #nay la kiem tra request data co dung chuan khong
            serializers.save()
            return Response(data=serializers.data, status=status.HTTP_200_OK)
        return Response(data= serializers.errors, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        client.delete()
        return Response(status.HTTP_204_NO_CONTENT)
    
        
    