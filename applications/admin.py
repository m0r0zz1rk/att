from django.contrib import admin
from import_export import resources, widgets
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from mptt.admin import MPTTModelAdmin
from .models import *


def duplicate(modeladmin, request, queryset):
    for rec in queryset:
        rec.id=None
        rec.save()

duplicate.short_description = 'Дублировать запись'


class SubjareasResource(resources.ModelResource):
    class Meta:
        model = Subjareas
        list_display = ("name",)


class PositionsResource(resources.ModelResource):
    class Meta:
        model = Position
        list_display = ("name_pos", "type_pos")


class MunobrResource(resources.ModelResource):
    class Meta:
        model = Munobr
        list_display = ("name_mo", "type_mo")


@admin.register(Munobr)
class MunobrAdmin(ImportExportModelAdmin):
    list_display = ('name_mo', 'type_mo')
    resource_class = MunobrResource


@admin.register(type_oo)
class TypeooAdmin(admin.ModelAdmin):
    list_display=('name',)


@admin.register(Attform)
class AttformAdmin(admin.ModelAdmin):
    list_display=('name',)


@admin.register(Stages)
class StagesAdmin(admin.ModelAdmin):
    list_display = ('name_stage',)


@admin.register(Criterias)
class CriteriasAdmin(MPTTModelAdmin):
    list_per_page = 500
    list_display=('name', 'description', 'need_upload', 'description_upload', 'description_crit')

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display=('name_cat',)

@admin.register(Parameters)
class ParametersAdmin(admin.ModelAdmin):
    list_display = ('parameter_name',)

@admin.register(CritPars)
class CritParsAdmin(admin.ModelAdmin):
    raw_id_fields = ("criteria",)
    search_fields = ('criteria__name', 'criteria__description', 'subj')
    list_display = ('criteria', 'get_params', 'subj')

    def get_params(self, obj):
        return "\n".join([c.parameter_name for c in obj.parameters.all()])

        def __str__(self):
            return 'Параметры'

@admin.register(Position)
class PositionAdmin(ImportExportModelAdmin):
    list_display=('name_pos',)
    resource_class = PositionsResource


@admin.register(Subjareas)
class SubjareasAdmin(ImportExportModelAdmin):
    list_display=('name',)
    resource_class = SubjareasResource


@admin.register(PosCriterias)
class PosCriteriasAdmin(admin.ModelAdmin):
    search_fields = ('pos__name_pos',)
    list_display = ('pos', 'get_crits')
    actions = [duplicate]

    def get_crits(self, obj):
        return "\n".join([c.name+' - '+c.description for c in obj.crits.all()])

        def __str__(self):
            return 'Критерии'
# Register your models here.
