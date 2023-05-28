"""Admin functionality for the BuildOrder app"""

from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export import widgets

from build.models import Build, BuildItem
from InvenTree.admin import InvenTreeResource
import part.models
<<<<<<< HEAD
=======
from django.http import HttpResponse
from django.contrib.admin.utils import get_fields_from_path

def export_admin_action(modeladmin, request, queryset):
    """
    Custom export action for the admin interface.
    This example exports the selected objects as a CSV file.
    """

    # Get the fields for the model
    fields = get_fields_from_path(modeladmin.model, None)

    # Create the CSV content
    csv_content = ','.join(field.name for field in fields) + '\n'
    for obj in queryset:
        csv_content += ','.join(str(getattr(obj, field.name)) for field in fields) + '\n'

    # Create the HTTP response with the CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="export.csv"'
    response.write(csv_content)

    return response

export_admin_action.short_description = "Export selected objects"
>>>>>>> 331c0c7ac41e8dd6ad8241f441a49bf3aa607e5c


class BuildResource(InvenTreeResource):
    """Class for managing import/export of Build data."""
    # For some reason, we need to specify the fields individually for this ModelResource,
    # but we don't for other ones.
    # TODO: 2022-05-12 - Need to investigate why this is the case!

    class Meta:
        """Metaclass options"""
        models = Build
        skip_unchanged = True
        report_skipped = False
        clean_model_instances = True
        exclude = [
            'lft', 'rght', 'tree_id', 'level',
            'metadata',
        ]

    id = Field(attribute='pk', widget=widgets.IntegerWidget())

    reference = Field(attribute='reference')

    title = Field(attribute='title')

    part = Field(attribute='part', widget=widgets.ForeignKeyWidget(part.models.Part))

    part_name = Field(attribute='part__full_name', readonly=True)

    overdue = Field(attribute='is_overdue', readonly=True, widget=widgets.BooleanWidget())

    completed = Field(attribute='completed', readonly=True)

    quantity = Field(attribute='quantity')

    status = Field(attribute='status')

    batch = Field(attribute='batch')

    notes = Field(attribute='notes')


class BuildAdmin(ImportExportModelAdmin):
    """Class for managing the Build model via the admin interface"""

    exclude = [
        'reference_int',
    ]

    list_display = (
        'reference',
        'title',
        'part',
        'status',
        'batch',
        'quantity',
    )

    search_fields = [
        'reference',
        'title',
        'part__name',
        'part__description',
    ]

    autocomplete_fields = [
        'parent',
        'part',
        'sales_order',
        'take_from',
        'destination',
    ]
<<<<<<< HEAD
=======
    actions = list(ImportExportModelAdmin.actions) + [export_admin_action]
>>>>>>> 331c0c7ac41e8dd6ad8241f441a49bf3aa607e5c


class BuildItemAdmin(admin.ModelAdmin):
    """Class for managing the BuildItem model via the admin interface"""

    list_display = (
        'build',
        'stock_item',
        'quantity'
    )

    autocomplete_fields = [
        'build',
        'bom_item',
        'stock_item',
        'install_into',
    ]


admin.site.register(Build, BuildAdmin)
admin.site.register(BuildItem, BuildItemAdmin)
