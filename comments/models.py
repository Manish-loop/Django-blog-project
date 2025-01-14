from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
from posts.models import Post

class Comment(models.Model):
    user      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)


    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")
    
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    
    
    
    