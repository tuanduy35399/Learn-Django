from django.db import models
from django.conf import settings
# Create your models here.
class PostModel(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    content= models.TextField(blank=False)
    # author= models.CharField(max_length=100, null=False, blank=False, unique=True)
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title