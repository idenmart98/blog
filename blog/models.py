from django.db import models
from django.shortcuts import reverse 
from time import time
from slugify import slugify
from django.contrib.auth.models import User


def gen_slug(s):
	new_slug = slugify(s)
	return new_slug + '-' + str(int(time()))

class ActiveeManager(models.Manager):	
	def get_queryset(self):
		return super().get_queryset().filter(active=True)


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

	all_objects = models.Manager()
	objects = ActiveeManager()


	
	def get_absolute_url(self):
		return reverse('post_detail_url', kwargs={'slug':self.slug })

	def get_update_url(self):
		return reverse('post_update_url', kwargs={'slug':self.slug })

	def get_delete_url(self):
		return reverse('post_delete_url', kwargs={'slug':self.slug })
	
	def get_addlike_url(self):
		return reverse('add_like_url', kwargs={'slug':self.slug })
	

	def get_comment_url(self):
		return reverse('comment_create_url', kwargs={'slug':self.slug })
	
	



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

class Comment(models.Model):
	parent_id = models.ForeignKey('Comment',related_name='childs',on_delete=models.CASCADE,blank=True,null=True)
	author = models.ForeignKey(User,on_delete=models.CASCADE ,db_index=True)
	post = models.ForeignKey(Post,on_delete=models.CASCADE ,db_index=True, related_name='comments',blank=True,null=True)
	content = models.TextField(blank=True, db_index=True)
	pub_date = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('addlike_comment_url', kwargs={'slug':self.post.slug, 'comment_id': self.id})

	def get_create_comment_url(self):
		return reverse('comment_commentcreate_url', kwargs={'slug':self.post.slug ,'comment_id' :self.id})
	def count_likes(self):
		return Likes.objects.filter(comment=self.id,likes=True).count()

	def count_dislikes(self):
		return Likes.objects.filter(comment=self.id,likes=False).count()

	class Meta:
		ordering = ['-pub_date']

class Likes(models.Model):
	likes = models.BooleanField()
	liker = models.ForeignKey(User,on_delete=models.CASCADE )
	post = models.ForeignKey(Post,on_delete=models.CASCADE ,blank=True,null=True, related_name='likes')
	comment = models.ForeignKey(Comment,on_delete=models.CASCADE,blank=True,null=True, related_name='likes')