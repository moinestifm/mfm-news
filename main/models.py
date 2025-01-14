from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

class Category(models.Model):
    title=models.CharField(max_length=200)
    category_image=models.ImageField(upload_to='imgs/')

    class Meta:
        verbose_name_plural ='Categories'

    def __str__(self):
        return self.title
    
class News(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    image = models.ImageField(upload_to='Imgs')
    description = models.CharField(max_length=300)
    article = RichTextUploadingField()
    add_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural ='News'

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    comment = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Comment by {self.name} on {self.created_at}"

    def __str__(self):
        return self.comment 