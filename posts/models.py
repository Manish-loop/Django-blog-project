from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import os
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from django.utils.text import slugify


from markdown import markdown


# Create your models here.
# way to control how model works= PostManager
class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename): # where images are actually uploaded to 
    return os.path.join(str(instance.id), filename)
    # return "%s/%s" %(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to=upload_location, 
            null=True, 
            blank=True, 
            width_field="width_field", 
            height_field="height_field")
    height_field = models.IntegerField(null=True, blank=True)
    width_field = models.IntegerField(null=True, blank=True)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    objects = PostManager() # Linking model manager to our model 
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})
        
    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)
    
    class Meta:
        ordering = ["-timestamp", "-updated"]
        
    
    
    

def create_slug(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    qs = Post.objects.filter(slug=slug).order_by("-id")
    if qs.exists():
        # new_slug = "%s-%s" % (slug, qs.first().id)
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

    def save_slug(sender, instance, **kwargs):
        if not instance.slug:
            instance.slug = create_slug(instance)
            instance.save()

    post_save.connect(save_slug, sender=Post)
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
    
pre_save.connect(pre_save_post_receiver, sender=Post) 