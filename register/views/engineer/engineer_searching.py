from register.models import Engineer
from django.conf import settings
from register.filters import EngineerFilter
from django_filters.views import FilterView
from braces.views import GroupRequiredMixin
from register.tables import EngineerTable
from django_tables2 import SingleTableView
from django.http import HttpResponse
from common.views import get_query_by_key
import csv


# for code that does the filtering (using django-filter) see /Users/stephenmcgonigal/django_projs/client/filters.py
# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
# https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html
# https://django-filter.readthedocs.io/en/develop/guide/usage.html#the-template
# restrict access: # https://github.com/brack3t/django-braces & http://django-braces.readthedocs.io/en/v1.4.0/access.html#loginrequiredmixin
class EngineerViewFilter(GroupRequiredMixin, FilterView, SingleTableView):
    group_required = [settings.APPROVER_GROUP, settings.ADMIN_GROUP]
    model = Engineer
    table_class = EngineerTable # /Users/stephenmcgonigal/django_projs/client/tables.py
    filterset_class = EngineerFilter # see /Users/stephenmcgonigal/django_projs/client/filters.py
    template_name='engineer/engineer_search.html'
    # see /Users/stephenmcgonigal/django_projs/cmenv/lib/python3.5/site-packages/django_tables2/client.py
    # SingleTableMixin class (SingleTableView inherits from it)
    table_pagination = {'per_page': 5}
    context_table_name = 'engineer_table'


    # renders template response rendered with passed in context
    # so I need to access table stuff
    # https://www.imagescape.com/blog/2016/03/03/django-class-based-views-basics/
    def get_context_data(self, **kwargs):
        # the context is passed into the template
        context = super(EngineerViewFilter, self).get_context_data(**kwargs)

        # setup csv file for download
        # https://simpleisbetterthancomplex.com/tutorial/2016/07/29/how-to-export-to-excel.html
        filtered_queries = context['object_list'] # with no pagination
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="engineers.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'ife_member_grade', 'first_name', 'last_name', 'address_line1', 'postcode', 'ife_member_no', 'ife_member_reg_date'])
        engineers = filtered_queries.values_list('id', 'user__first_name', 'user__last_name', 'address__line_1', 'address__post_code', 'ife_member_grade', 'ife_member_no', 'ife_member_reg_date')
        for engineer in engineers:
            writer.writerow(engineer)
        context['csv_response'] = response
        return context

    def get(self, request, *args, **kwargs):
        # the line between ---> and <---- were taken from cmenv/lib/python3.5/site-packages/django_filters/views.py
        # --->
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)
        self.object_list = self.filterset.qs
        context = self.get_context_data(filter=self.filterset,
                                        object_list=self.object_list)
        # <----
        csv_reqd = get_query_by_key(request, 'csv_reqd')
        if csv_reqd is not None:
            return context['csv_response']
        else:
            return self.render_to_response(context)
