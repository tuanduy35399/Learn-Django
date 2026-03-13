from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.
class TodoModel(models.Model):
    title =models.CharField(max_length=100, null= False)
    body= models.TextField(default="", blank= True)
    image= CloudinaryField('image')
    createdAt= models.DateTimeField(auto_now_add=True)
    updatedAt= models.DateTimeField(auto_now=True)
    isCompleted= models.BooleanField(default= False)

    def __str__(self):
        return self.title
    

