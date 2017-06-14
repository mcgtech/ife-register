from register.models import Engineer
from django_tables2 import tables, LinkColumn, A

class EngineerTable(tables.Table):
    # https://stackoverflow.com/questions/33184108/how-to-change-display-text-in-django-tables-2-link-column
    # http://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#linkcolumn
    engineer_id = LinkColumn('engineer_edit', text=lambda record: record.id, args=[A('pk')], attrs={'a': {'target': '_blank'}})

    class Meta:
        model = Engineer
        # fields to display in table
        fields = ('forename',)
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('engineer_id', '...',)