
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

    def __str__(self):
        return self.title
#use for tags 
only_aphabets =  RegexValidator(r'^[, a-zA-Z]*$', 'Enter comma separated tags. (use space for two words tag)')        
class Post(models.Model):
    title = models.CharField(max_length=100)
    overview = RichTextUploadingField()
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
            'pk': self.pk
        })
# you would access your hit_count like so:
                # total number of hits
# my_model.hit_count.hits_in_last(days=7) # number of hits in last seven days        