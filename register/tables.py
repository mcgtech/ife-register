from register.models import Engineer
from django_tables2 import tables, LinkColumn, A, Column

class EngineerTable(tables.Table):
    # https://stackoverflow.com/questions/33184108/how-to-change-display-text-in-django-tables-2-link-column
    # http://django-tables2.readthedocs.io/en/latest/pages/api-reference.html#linkcolumn
    engineer_id = LinkColumn('engineer_edit', text=lambda record: record.id, args=[A('pk')], attrs={'a': {'target': '_blank'}})
    full_name = Column(empty_values=(), verbose_name='Name', orderable= False)
    submission_date = Column(empty_values=(), verbose_name='Submission Date', orderable= False)
    current_status = Column(empty_values=(), verbose_name='Current Status', orderable= False)
    ife_member_grade = Column(verbose_name='IFE Grade')

    def render_full_name(self, record):
        return record.get_full_name()

    def render_submission_date(self, record):
        return record.get_submission_date()

    def render_current_status(self, record):
        latest = record.get_latest_status()
        return latest.get_status_display if latest is not None else None


    class Meta:
        model = Engineer
        # fields to display in table
        fields = ('employer', 'ife_member_grade')
        attrs = {"class": "paleblue table table-striped table-hover table-bordered"}
        sequence = ('engineer_id', 'full_name', 'current_status', 'submission_date', 'ife_member_grade', '...',)