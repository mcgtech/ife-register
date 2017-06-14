from register.models import Engineer
from django.conf import settings
from register.filters import EngineerFilter
from django_filters.views import FilterView
from braces.views import GroupRequiredMixin
from register.tables import EngineerTable
from django_tables2 import SingleTableView



# for code that does the filtering (using django-filter) see /Users/stephenmcgonigal/django_projs/client/filters.py
# https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
# https://simpleisbetterthancomplex.com/2015/12/04/package-of-the-week-django-widget-tweaks.html
# https://django-tables2.readthedocs.io/en/latest/pages/tutorial.html
# https://django-filter.readthedocs.io/en/develop/guide/usage.html#the-template
# restrict access: # https://github.com/brack3t/django-braces & http://django-braces.readthedocs.io/en/v1.4.0/access.html#loginrequiredmixin
class EngineerViewFilter(GroupRequiredMixin, FilterView, SingleTableView):
    group_required = [settings.ADMIN_GROUP]
    model = Engineer
    table_class = EngineerTable # /Users/stephenmcgonigal/django_projs/client/tables.py
    filterset_class = EngineerFilter # see /Users/stephenmcgonigal/django_projs/client/filters.py
    template_name='engineer/engineer_search.html'
    # see /Users/stephenmcgonigal/django_projs/cmenv/lib/python3.5/site-packages/django_tables2/client.py
    # SingleTableMixin class (SingleTableView inherits from it)
    table_pagination = {'per_page': 15}
    context_table_name = 'engineer_table'
