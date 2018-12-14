from django.urls import path
from .views import *

urlpatterns = [
	path('',post_list,name='post_list_url'),
	path('posts/create',post_create,name='post_create_url'),
	path('posts/<str:slug>/', post_detail, name='post_detail_url'),
	path('posts/<str:slug>/update',post_update,name='post_update_url'),
	path('tags/',tag_list, name='tags_list_url'),
	path('tags/create',tag_create, name='tag_create_url'),
	path('tags/<str:slug>/',tag_detail,name='tag_detail_url'),
	path('tags/<str:slug>/update',tag_update,name='tag_update_url'),
	path('tags/<str:slug>/delete',tag_delete,name='tag_delete_url'),
	path('posts/<str:slug>/delete',post_delete,name='post_delete_url'),
	path('post/<str:slug>/addlikes',add_likes,name='add_like_url'),
	path('post/<str:slug>/coment',coment_create,name ='coment_create_url')
	

	


	
]