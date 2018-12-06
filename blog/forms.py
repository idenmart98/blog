from django import forms
from blog.models import *

class PostCreateForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title','body','tags']

		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control'}),
			'body': forms.Textarea(attrs={'class':'form-control'}),
			'tags': forms.SelectMultiple(attrs={'class':'form-control'}),
			}

	# def __init__(self, *args, **kwargs): 
	# 	author = kwargs.pop('user', None) # pop the 'user' from kwargs dictionary      
	# 	super(PostCreateForm, self).__init__(*args, **kwargs)
	# 	self.fields['posts'] = forms.ModelChoiceField(queryset=Post.objects.filter(author=user)

class TagCreateForm(forms.ModelForm):
	class Meta:
		model = Tag
		fields = ['title']

		widgets = {
		'title': forms.TextInput(attrs={'class':'form-control'}),
		}
