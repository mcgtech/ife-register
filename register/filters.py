from register.models import Engineer
import django_filters
from django.db.models import Q

class EngineerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name', name='name', label='Name')
    employer = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Engineer
        fields = ['employer']

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(user__first_name__contains=value) | Q(user__last_name__contains=value))