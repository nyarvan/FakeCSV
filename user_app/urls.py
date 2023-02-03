from django.urls import path
from .views import SchemasView, SchemeDetailView, NewSchemaView, EditSchemaView, delete_schema, delete_column

app_name = 'user_app'

urlpatterns = [
    path('', SchemasView.as_view(), name='schemas'),
    path('new-schema', NewSchemaView.as_view(), name='new_schema'),
    path('scheme/<pk>', SchemeDetailView.as_view(), name='scheme'),
    path('scheme/<pk>/update', EditSchemaView.as_view(), name='update_schema'),
    path('scheme/<pk>/delete', delete_schema, name='delete_schema'),
    path('scheme/delete-column/<pk>', delete_column, name='delete_column')
]
