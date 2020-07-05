
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from ckeditor.fields import  RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# for hitcount
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCount, HitCountMixin
# for tag 
from django.core.validators import RegexValidator

User = get_user_model()

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('posts_in_category', kwargs={
            'slug': self.slug
        })
    
    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.capitalize()

        super(Category, self).save(*args, **kwargs)    
#use for tags 
only_aphabets =  RegexValidator(r'^[, a-zA-Z]*$', 'Enter comma separated tags. (use space for two words tag)')        
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    overview = RichTextUploadingField(null=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default = 0)
    tags = models.CharField(max_length=60, blank=True, validators=[only_aphabets])
    # 3rd party field
    hit_count = GenericRelation(
                HitCount, object_id_field='object_pk',
                related_query_name='hit_count_generic_relation')
    # view_count = models.IntegerField(default = 0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)
    featured = models.BooleanField()
    previous_post = models.ForeignKey(
        'self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_post = models.ForeignKey(
        'self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)

   
    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={
            'slug': self.slug
        })
class Comment(models.Model): 
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80) 
    email = models.EmailField() 
    body = models.TextField() 
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True) 
    active = models.BooleanField(default=True) 
 
    class Meta: 
        ordering = ('created',) 
 
    def __str__(self): 
        return 'Comment by {} on {}'.format(self.name, self.post)        
class About(models.Model):
    overview = RichTextUploadingField()
    image = models.ImageField(upload_to='uploads/')        
# you would access your hit_count like so:
                # total number of hits
# my_model.hit_count.hits_in_last(days=7) # number of hits in last seven days        