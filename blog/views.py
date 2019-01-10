from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views.generic import View,ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Prefetch, Count, Subquery, IntegerField, OuterRef
from django.http import HttpResponse
from django.utils.timezone import datetime

from blog.models import Post,Tag,Comment,Likes
from blog.utils import ObjectDetailMixin
from blog.filters import *
from blog.forms import *

from datetime import datetime, timedelta


def add_likes(request, slug):

	post = get_object_or_404(Post,slug=slug)
	
	if request.user.is_authenticated :
		if not Likes.objects.filter(post = post ,liker = request.user):
			if request.GET:
				like = request.GET.get('like') == 'like'
				Likes.objects.create(post =post, likes=like, liker=request.user)
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))

		if Likes.objects.filter(post = post ,liker = request.user):
			like = Likes.objects.filter(post = post ,liker = request.user)
			
			like.delete()
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
		else:
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
		
	else:
		return render(request, 'blog/iden.html' )

class SQCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = IntegerField()

 

def post_detail(request, slug):
	likes = Likes.objects.filter(post=OuterRef('id')).values('id')

	comment_likes = Likes.objects.filter(comment=OuterRef('id')).values('id')
	comments = Comment.objects.annotate(likes_count=SQCount(comment_likes.filter(likes=True)), 
								 dislikes_count=SQCount(comment_likes.filter(likes=False)))
	post = Post.objects.prefetch_related(Prefetch('comments', queryset=comments, to_attr='comment_objects'), 'comments').\
						annotate(likes_count=SQCount(likes.filter(likes=True)), 
								dislikes_count=SQCount(likes.filter(likes=False))).\
						get(slug=slug)

						
	return render(request, 'blog/post_detail.html', {'post': post})

def tag_detail(request, slug):
	tag = get_object_or_404(Tag, slug=slug)
	return render(request, 'blog/tag_detail.html',{'tag':tag})

def tag_create(request):

	if request.method == 'GET':
		form = TagForm()
		return render(request, 'blog/tag_create.html', {'form':form})

	if request.method == 'POST':

		bound_form = TagForm(request.POST)
		if bound_form.is_valid():
			new_tag = bound_form.save()
			return redirect(new_tag)
		return render(request, 'blog/tags_list.html')

def post_create(request):
	if request.method == 'GET':
		form = PostForm()
		return render(request, 'blog/post_create.html', {'form': form})

	if request.method == 'POST':
		bound_form = PostForm(request.POST)
		if bound_form.is_valid():
		
			bound_form.instance.author = request.user
			new_post = bound_form.save()
			
			posts = Post.objects.all()
			return render(request, 'blog/index.html', {'posts':posts})





def post_list(request):
	search_query = request.GET.get('search','')
	if search_query:
		posts = Post.objects.filter(Q(title__icontains=search_query)|Q(body__icontains=search_query), ) 
		return render(request, 'blog/index.html', {'posts':posts})
	else:
		posts = Post.objects.all()
		return render(request, 'blog/index.html', {'posts':posts})



def tag_list(request):
	tags = Tag.objects.all()
	return render(request, 'blog/tags_list.html', {'tags':tags})

 
def tag_update(request, slug):
	if request.method == 'GET':
		tag = Tag.objects.get(slug__iexact=slug)
		bound_form = TagForm(instance=tag)
		return render(request, 'blog/tag_update.html', {'form':bound_form, 'tag':tag})

	if request.method == 'POST':
		tag = Tag.objects.get(slug__iexact=slug)
		bound_form = TagForm(request.POST, instance=tag)

		if bound_form.is_valid():
			new_tag = bound_form.save()
			return redirect(new_tag)
		return render(request.POST, 'blog/tag_update.html', {'form':bound_form,'tag':tag})




def post_update(request,slug):
	if request.method == 'GET':
		post = Post.objects.get(slug__iexact=slug)
		bound_form = PostForm(instance=post)
		return render(request, 'blog/post_update.html', {'form':bound_form, 'post':post})

	if request.method =='POST':
		post = Post.objects.get(slug__iexact=slug)
		bound_form = PostForm(request.POST, instance=post)

		if bound_form.is_valid():
			new_post = bound_form.save()
			return redirect(new_post)
		return render(request.POST, 'blog/post_update.html', {'form':bound_form, 'post':post})



def post_delete(request,slug):
	if request.method == 'GET':
		post = Post.objects.get(slug__iexact=slug)
		return render(request, 'blog/post_delete.html', {'post':post})

	if request.method == 'POST':
		post = Post.objects.get(slug__iexact=slug)
		post.delete()
		return redirect(reverse('post_list_url'))



def tag_delete(request, slug):
	if request.method == 'GET':
		tag = Tag.objects.get(slug__iexact=slug)
		return render(request, 'blog/tag_delete.html', {'tag':tag})

	if request.method == 'POST':
		tag = Tag.objects.get(slug__iexact=slug)
		tag.delete()
		return redirect(reverse('tags_list_url'))

def comment_commentcreate(request,comment_id,slug):
	comm_id = Comment.objects.get(id=comment_id)
	post = Post.objects.get(slug__iexact=slug)
	if request.user.is_authenticated:
		if request.method =='GET':
			
			return render(request,'blog/comment_create.html')
		if request.method == 'POST':
			comment = request.POST.get('content')
			Comment.objects.create(post = post,parent_id=comm_id,author=request.user, content=comment,)
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
	else:
		return render(request, 'blog/iden.html')
	
def comment_create(request,slug):
	post = Post.objects.get(slug__iexact=slug)
	if request.user.is_authenticated :
		if request.method == 'GET':
		
			return render(request,'blog/comment_create.html')
		if request.method == 'POST':
			comment = request.POST.get('content') 
			Comment.objects.create(post=post, author=request.user, content=comment)
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
	else:
		return render(request, 'blog/iden.html')

def addlike_comment(request,slug,comment_id):
	comment = Comment.objects.get(id=comment_id)
	
	post = get_object_or_404(Post,slug=slug)
	
	if request.user.is_authenticated :
		if not Likes.objects.filter(comment=comment, liker=request.user):
			if request.GET:
				like = request.GET.get('like') == 'like'
				print('hi')
				Likes.objects.create(comment = comment, likes=like, liker=request.user)
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))

		if Likes.objects.filter(comment = comment ,liker = request.user):
			like = Likes.objects.filter(comment = comment ,liker = request.user)
			
			like.delete()
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
		else:
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
		
	else:
		return render(request, 'blog/iden.html' )


def likes_count(request):
	
	l = Post.all_objects.all()
	for i in l:
		print(i.title)
		print(i.date_pub)
	# print (l)
	# print(datetime.now)