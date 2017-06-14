from register.models import Engineer
import django_filters

class EngineerFilter(django_filters.FilterSet):
    forename = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Engineer
        fields = ['forename']
