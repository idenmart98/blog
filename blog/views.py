from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views.generic import View,ListView,CreateView,UpdateView,DeleteView
from blog.models import Post,Tag,Coment,Likes
from blog.utils import ObjectDetailMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.filters import *
from blog.forms import *
from django.db.models import Q


def add_likes(request, slug):

	post = get_object_or_404(Post,slug=slug)
	
	if request.user.is_authenticated :
		if not Likes.objects.filter(post_id = post ,liker = request.user):
			if request.GET:
				like = request.GET.get('like') == 'like'
				Likes.objects.create(post_id=post, likes=like, liker=request.user)
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
		else:
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
	else:
		return render(request, 'blog/iden.html' )


def post_detail(request, slug):

	post = get_object_or_404(Post, slug=slug)
	coments =Coment.objects.filter(post_id=post)
	like = Likes.objects.filter(likes=True, post_id=post).count()
	dislike = Likes.objects.filter(likes=False, post_id=post).count()
	return render(request, 'blog/post_detail.html', {'post': post, 'like': like, 'dislike': dislike ,'coments':coments})

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
			return redirect(new_post)
		return render(request, 'blog/post_list.html')



def post_list(request):
	search_query = request.GET.get('search','')
	if search_query:
		posts = Post.activ.filter(Q(title__icontains=search_query)|Q(body__icontains=search_query), ) 
		return render(request, 'blog/index.html', {'posts':posts})
	else:
		posts = Post.activ.all()
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
		post = Post.activ.get(slug__iexact=slug)
		bound_form = PostForm(instance=post)
		return render(request, 'blog/post_update.html', {'form':bound_form, 'post':post})

	if request.method =='POST':
		post = Post.activ.get(slug__iexact=slug)
		bound_form = PostForm(request.POST, instance=post)

		if bound_form.is_valid():
			new_post = bound_form.save()
			return redirect(new_post)
		return render(request.POST, 'blog/post_update.html', {'form':bound_form, 'post':post})



def post_delete(request,slug):
	if request.method == 'GET':
		post = Post.activ.get(slug__iexact=slug)
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


	
def coment_create(request,slug):
	post = Post.activ.get(slug__iexact=slug)
	if request.user.is_authenticated :
		if request.method == 'GET':
		
			return render(request,'blog/coment_create.html')
		if request.method == 'POST':
			coment = request.POST.get('content') 
			Coment.objects.create(post_id=post,author_id=request.user,content=coment)
			return redirect(reverse('post_detail_url', kwargs={'slug': slug}))
	else:
		return render(request, 'blog/iden.html')


