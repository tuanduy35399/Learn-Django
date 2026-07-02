from rest_framework import status
from .post_serializers import PostV1Serializer
from app.models import Post
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
         post = Post.objects.all()
         serializers = PostV1Serializer(post, many=True)
         return Response(data= serializers.data, status= status.HTTP_200_OK)
    elif request.method == 'POST':
        serializers = PostV1Serializer(data= request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data= serializers.data, status = status.HTTP_201_CREATED)
        return Response(data = serializers.errors, status = status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk):
    try: 
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializers = PostV1Serializer(post)
        return Response(data= serializers.data,status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializers = PostV1Serializer(post, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(data= serializers.data, status= status.HTTP_200_OK)
        return Response(data= serializers.error, status= status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)