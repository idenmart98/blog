from django.db import models
from django.shortcuts import reverse 
from time import time
from django.utils.text import slugify
from django.contrib.auth.models import User


def gen_slug(s):
	new_slug = slugify(s, allow_unicode=True)
	return new_slug + '-' + str(int(time()))

class ActiveeManager(models.Manager):	
	def get_queryset(self):
		return super().get_queryset().filter(active = True)


# Create your models here.
class Post(models.Model):
	"""docstring for Post"""
	title = models.CharField(max_length=150,db_index=True)
	slug = models.SlugField(max_length=150,blank=True,unique=True)
	tags = models.ManyToManyField('Tag',blank=True,related_name='posts')
	body = models.TextField(blank=True, db_index=True)
	date_pub = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE ,db_index=True)
	active = models.BooleanField(default=False)

	objects = models.Manager()
	activ = ActiveeManager()


	
	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug':self.slug })

	def get_update_url(self):
		return reverse('post_update_url', kwargs={'slug':self.slug })

	def get_delete_url(self):
		return reverse('post_delete_url', kwargs={'slug':self.slug })
	
	def get_addlike_url(self):
		return reverse('add_like_url', kwargs={'slug':self.slug })
	

	def get_coment_url(self):
		return reverse('coment_create_url', kwargs={'slug':self.slug })
	
	



	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.title
	
	class Meta:
		ordering = ['-date_pub']
	

class Tag(models.Model):
	title = models.CharField(max_length=50,unique=True)
	slug = models.SlugField(max_length=50,unique=True)

	def get_absolute_url(self):
		return reverse('tag_detail_url', kwargs={'slug': self.slug})

	def get_update_url(self):
		return reverse('tag_update_url', kwargs={'slug':self.slug })

	def get_delete_url(self):
		return reverse('tag_delete_url', kwargs={'slug':self.slug })

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = gen_slug(self.title)
		super().save(*args, **kwargs)

	class Meta:
		ordering = ['title']

	def __str__(self):
		return '{}'.format(self.title)

class Coment(models.Model):
	author_id = models.ForeignKey(User,on_delete=models.CASCADE ,db_index=True)
	post_id = models.ForeignKey(Post,on_delete=models.CASCADE ,db_index=True)
	content = models.TextField(blank=True, db_index=True)
	pub_date = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-pub_date']

class Likes(models.Model):
	likes = models.BooleanField()
	liker = models.ForeignKey(User,on_delete=models.CASCADE )
	post_id = models.ForeignKey(Post,on_delete=models.CASCADE )