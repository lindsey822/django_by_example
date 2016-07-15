from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
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
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250, 
		                    unique_for_date='publish')
	# ForeignKey defines a many-to-one relationship
	# specify the name of the reverse relationship with related_name field
	# default column name: author_id
	author = models.ForeignKey(User,
		                       related_name='blog_posts')
	body = models.TextField()
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
		                      choices=STATUS_CHOICES, 
		                      default='draft')

	objects = models.Manager()
	published = PublishedManager() # custom manager

	class Meta:
		ordering = ('-publish',)

	def __str__(self):
		return self.title