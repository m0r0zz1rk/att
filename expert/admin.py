from django.contrib import admin
from import_export import resources, widgets
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from mptt.admin import MPTTModelAdmin
from .models import *


@admin.register(Experts)
class ExpertsAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'patronymic', 'mo', 'oo', 'subj', 'pos', 'email', 'snils', 'status')


@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('pos', 'criteria', 'mark_list')
    search_fields = ('pos__name_pos', 'criteria__name')


@admin.register(Total)
class TotalAdmin(admin.ModelAdmin):
    list_display = ('cat', 'pos', 'total')
    search_fields = ('pos__name_pos', )
