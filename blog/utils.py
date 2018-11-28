from django.shortcuts import render,get_object_or_404
from django.views.generic import DetailView



class ObjectDetailMixin(DetailView):
	template_name = None
	model = None
	objec = None
	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		context['model'] = get_object_or_404(self.model, slug=self.kwargs['slug'])
		return context
	# def get (self,request,slug):
	# 	obj = get_object_or_404(self.model, slug__iexact=slug)
	# 	return render(request,self.template,context = {self.model.__name__.lover():obj})
