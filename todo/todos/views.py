from rest_framework import viewsets
from .models import TodoModel
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = TodoModel.objects.all()
    serializer_class= TodoSerializer

