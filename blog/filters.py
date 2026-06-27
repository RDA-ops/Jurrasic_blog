import django_filters
from .models import Article, Category

class ArticleFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Название')
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория'
    )
    created_at = django_filters.DateFromToRangeFilter(label='Дата создания')

    class Meta:
        model = Article
        fields = ['title', 'category', 'created_at']