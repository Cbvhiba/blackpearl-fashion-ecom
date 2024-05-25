from django.db import models
from django_lifecycle import LifecycleModelMixin
import uuid
from django.utils.text import slugify
import random
import string


class BaseModel(LifecycleModelMixin,models.Model):
    display_name = 'name'
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    status = models.CharField(default='Active',max_length=20, choices=(
        ('Active','Active'),
        ('Inactive','Inactive')
    ))
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance,slugField, new_slug = None): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(slugField) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = 5)) 
              
        return unique_slug_generator(instance,slugField, new_slug = new_slug) 
    return slug 