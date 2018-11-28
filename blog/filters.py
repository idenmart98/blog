from django.db.models import Q
import django_filters

from blog.models import Post

class PostFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_post')

    class Meta:
        model = Post
        fields = ['title','body']

    def search_post(self, queryset, name, value):
    	return queryset.filter(
    		Q(title__icontains=value) | Q(body__icontains=value)).distinct()