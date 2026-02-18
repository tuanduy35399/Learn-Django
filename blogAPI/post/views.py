from .models import PostModel
from .serializers import PostSerializer
from rest_framework import viewsets
# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class= PostSerializer
