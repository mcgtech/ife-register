from register.models import Engineer
from django_tables2 import tables, LinkColumn, A, Column

class EngineerTable(tables.Table):
    # https://stackoverflow.com/questions/33184108/how-to-change-display-text-in-django-tables-2-link-column
    # http://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#linkcolumn
    engineer_id = LinkColumn('engineer_edit', text=lambda record: record.id, args=[A('pk')], attrs={'a': {'target': '_blank'}})
    full_name = Column(empty_values=(), verbose_name='Name', orderable= False)

    def render_full_name(self, record):
        return record.get_full_name()


    class Meta:
        model = Engineer
        # fields to display in table
        fields = ('title',)
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('engineer_id', '...',)