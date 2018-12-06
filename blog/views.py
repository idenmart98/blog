from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views.generic import View,ListView,CreateView,UpdateView,DeleteView
from blog.models import Post,Tag
from blog.utils import ObjectDetailMixin
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.filters import *
from blog.forms import *







class TagDetail(ObjectDetailMixin):
	template_name = 'blog/tag_detail.html'
	model=Tag
	
class PostDetail(ObjectDetailMixin):
	template_name = 'blog/post_detail.html'
	model = Post

class TagCreate(LoginRequiredMixin,CreateView):
	model = Tag
	form_class = TagCreateForm
	template_name = 'blog/tag_create.html'
	raise_exception = True


class PostList(ListView):
	model = Post
	template_name = 'blog/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['posts'] = PostFilter(self.request.GET, queryset=Post.objects.all())
		return context


	

class TagList(ListView):
	model = Tag
	template_name = 'blog/tags_list.html'
	


class PostCreate(LoginRequiredMixin,CreateView):
	model = Post
	
	template_name = 'blog/post_create.html'
	raise_exception = True
	form_class = PostCreateForm
	
	def form_valid(self, form):
		form.instance.author = self.request.user
		return super(PostCreate, self).form_valid(form) 


class TagUpdate(LoginRequiredMixin,UpdateView):
	model = Tag
	template_name = 'blog/tag_update.html'
	fields =['title']
	raise_exception = True

class PostUpdate(LoginRequiredMixin,UpdateView):
	model = Post
	template_name = 'blog/post_update.html'
	fields = ['title','body','tags']
	raise_exception = True

class PostDelete(LoginRequiredMixin,DeleteView):
	model = Post
	template_name = 'blog/post_delete.html'
	success_url = reverse_lazy('post_list_url')
	raise_exception = True

class TagDelete(LoginRequiredMixin,DeleteView):
	model = Tag
	template_name = 'blog/tag_delete.html'
	success_url = reverse_lazy('tags_list_url')
	raise_exception = True



