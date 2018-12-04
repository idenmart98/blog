from django.http import HttpResponse
from django.shortcuts import redirect
from blogin.views import *
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout




def redirect_blog (request):
	return redirect('post_list_url',permanent = True)



class RegisterFormView(FormView):

	form_class = UserCreationForm
	success_url = '/login/'
	template_name = "register.html"

	def form_valid(self, form):
      
		form.save()
		return super(RegisterFormView, self).form_valid(form)

	def get(self, *args, **kwargs):			
		if self.request.user.is_authenticated:
			return redirect('post_list_url')
		return super().get(*args, **kwargs)		






class LoginFormView(FormView):
		
	form_class = AuthenticationForm
	template_name = "login.html"
	success_url = '/'
	def form_valid(self, form):
	        
		self.user = form.get_user()
		login(self.request, self.user)
		return super(LoginFormView, self).form_valid(form)

	def get(self, *args, **kwargs):			
		if self.request.user.is_authenticated:
			return redirect('post_list_url')
		return super().get(*args, **kwargs)		


class LogoutView(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect("/")