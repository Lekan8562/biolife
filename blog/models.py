from django.db import models
from django.contrib.auth.models import User
from froala_editor.fields import FroalaField

class Post(models.Model):
     title = models.CharField(max_length=250)
     slug = models.SlugField(max_length=250)
     tag = models.ManyToManyField('Tag', related_name='posts')
     image = models.ImageField(upload_to = 'blog_images/',null = True,blank = True)
     author = models.ForeignKey(User,on_delete=models.CASCADE)
     pub_date = models.DateTimeField(auto_now_add=True)
     updated = models.DateTimeField(auto_now=True)
     body = FroalaField()
     quote = models.TextField(null=True, blank=True)
     def __str__(self):
         return self.title
     
     class Meta:
         verbose_name = 'posts'
         ordering = ['-pub_date']
         get_latest_by = 'title'
 

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.body
    class Meta:
        ordering = ['-date']
    
class Reply(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE)
    class Meta:
        ordering = ['-date']
    def __str__(self):
        return self.body
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'tag'
        ordering = ['name']
