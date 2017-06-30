from register.models import Engineer, ApplicationStatus
import django_filters
from django.db.models import Q

class EngineerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='filter_name', name='name', label='Name')
    employer = django_filters.CharFilter(lookup_expr='icontains')
    sub_from = django_filters.DateFilter(method='filter_sub_from', name='sub_from', label='Submitted >=')
    status = django_filters.ChoiceFilter(choices=ApplicationStatus.STATUS, method='filter_app_status', name='app_status', label='Status')

    class Meta:
        model = Engineer
        fields = ['employer']

    def filter_name(self, queryset, name, value):
        return queryset.filter(Q(user__first_name__contains=value) | Q(user__last_name__contains=value))

    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_sub_from(self, queryset, name, value):
        eng_ids = []
        for eng in queryset:
            sub_date = eng.get_submission_date()
            if sub_date is not None and sub_date.date() >= value:
                eng_ids.append(eng.id)
        return queryset.filter(pk__in=eng_ids)


    # https://stackoverflow.com/questions/42526670/django-filter-on-values-of-child-objects
    def filter_app_status(self, queryset, name, value):
        eng_ids = []
        for eng in queryset:
            latest_status = eng.get_latest_status()
            if latest_status is not None and int(latest_status.status) == int(value):
                eng_ids.append(eng.id)
        return queryset.filter(pk__in=eng_ids)