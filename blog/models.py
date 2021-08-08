"""
Data models of your application—all Django applications need to have a models.py file, but this file can be left empty.
"""

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
        self).get_queryset()\
             .filter(status='published')

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        )
    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250,
                            unique_for_date = 'publish')
    author = models.ForeignKey(User,
                               on_delete = models.CASCADE,
                               related_name='blog_post')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()
    
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                        args=[self.publish.year,
                              self.publish.month,
                              self.publish.day,
                              self.slug])

    class Meta:
        ordering = ('-publish',)
        
    def __str__(self):
        return self.title

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
        return f'Comment by {self.name} on {self.post}'




"""
title: 
    This is the field for the post title. This field is CharField, which translates into a VARCHAR column in the SQL database.

slug: 
    This is a field intended to be used in URLs. A slug is a short label that contains only letters, numbers, underscores, or hyphens. We will use the slug field to build beautiful, SEO-friendly URLs for our blog posts. We have added the unique_for_date parameter to this field so that we can build URLs for posts using their publish date and slug. Django will prevent multiple posts from having the same slug for a given date.

author: 
    This field is a foreign key. It defines a many-to-one relationship. We are telling Django that each post is written by a user, and a user can write any number of posts. For this field, Django will create a foreign key in the database using the primary key of the related model. In this case, we are relying on the User model of the Django authentication system. The on_delete parameter specifies the behavior to adopt when the referenced object is deleted. This is not specific to Django; it is an SQL standard. Using CASCADE, we specify that when the referenced user is deleted, the database will also delete its related blog posts. You can take a look at all possible options at https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.ForeignKey.on_delete. We specify the name of the reverse relationship, from User to Post, with the related_name attribute. This will allow us to access related objects easily. We will learn more about this later.

body: 
    This is the body of the post. This field is a text field, which translates into a TEXT column in the SQL database.

publish: 
    This datetime indicates when the post was published. We use Django's timezone now method as the default value. This returns the current datetime in a timezone-aware format. You can think of it as a timezone-aware version of the standard Python datetime.now method.

created: 
    This datetime indicates when the post was created. Since we are using auto_now_add here, the date will be saved automatically when creating an object.

updated: 
    This datetime indicates the last time the post was updated. Since we are using auto_now here, the date will be updated automatically when saving an object.

status: 
    This field shows the status of a post. We use a choices parameter, so the value of this field can only be set to one of the given choices.
"""   