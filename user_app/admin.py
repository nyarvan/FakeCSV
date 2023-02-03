from django.contrib import admin
from .models import Type, Column, Schema, FileCSV


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'from_range', 'to_range']
    list_editable = ['from_range', 'to_range']


class ColumnAdmin(admin.TabularInline):
    model = Column
    raw_id_fields = ['schema', ]


@admin.register(Schema)
class SchemaAdmin(admin.ModelAdmin):
    list_display = ['name', 'column_separator', 'string_character']
    list_display_links = ['name', ]
    list_editable = ['column_separator', 'string_character']
    search_fields = ['name', ]
    inlines = [ColumnAdmin, ]


@admin.register(FileCSV)
class FileCSVAdmin(admin.ModelAdmin):
    list_display = ['created', 'schema', 'status', 'file']
    list_editable = ['status', ]
    search_fields = ['created', 'schema']
