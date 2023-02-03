from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Schema, Column, Type, FileCSV
from .forms import SchemaForm, ColumnFormSet
from django.shortcuts import get_object_or_404
import csv
import uuid
from django.http import HttpResponse
from .utils import generate_row
from django.conf import settings


class SchemaInline():
    form_class = SchemaForm
    model = Schema
    template_name = "add_schema.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        if not self.object:
            Schema.objects.create(user=self.request.user, **form.cleaned_data)
        else:
            self.object = form.save()

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('user_app:schemas')

    def formset_column_valid(self, formset):
        columns = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for column in columns:
            column.schema = self.object
            column.save()


class SchemasView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    template_name = 'schemas.html'
    context_object_name = 'schemas'
    allow_empty = True

    def get_queryset(self):
        return Schema.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SchemeDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    template_name = 'schema.html'
    model = Schema
    context_object_name = 'scheme'
    queryset = Schema.objects.all()        

    def get(self, request, *args, **kwargs):
        if self.request.GET.get('rows'):
            rows = int(self.request.GET['rows'])
            columns = Column.objects.filter(schema=self.get_object())
            
            fieldnames = [column.name for column in columns]
            file_name = f'{self.get_object().user}-{self.get_object().name}-{uuid.uuid4()}.csv'

            with open(f'{settings.MEDIA_ROOT}/{file_name}', 'w') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for _ in range(rows):
                    row = generate_row(columns)
                    writer.writerow(row)

            FileCSV.objects.create(schema=self.get_object(), status=True, file=f'{settings.MEDIA_ROOT}/{file_name}')

            return redirect('user_app:scheme', pk=self.get_object().pk)

        return super().get(request, *args, **kwargs)
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['columns'] = Column.objects.filter(schema=self.get_object())
        context['csv_files'] = FileCSV.objects.filter(schema=self.get_object()) 
        return context


class NewSchemaView(LoginRequiredMixin, SchemaInline, CreateView):
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        ctx = super(NewSchemaView, self).get_context_data(**kwargs)
        ctx['types'] = Type.objects.all()
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'columns': ColumnFormSet(prefix='columns'),
            }
        else:
            return {
                'columns': ColumnFormSet(self.request.POST or None, self.request.FILES or None, prefix='columns'),
            }


class EditSchemaView(LoginRequiredMixin, SchemaInline, UpdateView):
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        ctx = super(EditSchemaView, self).get_context_data(**kwargs)
        ctx['types'] = Type.objects.all()
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'columns': ColumnFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='columns'),
        }


@login_required(login_url="/login/")
def delete_schema(request, pk):
    schema = get_object_or_404(Schema, pk=pk)
    schema.delete()
    return redirect('user_app:schemas')


@login_required(login_url="/login/")
def delete_column(request, pk):
    column = get_object_or_404(Column, pk=pk)
    column.delete()
    return redirect('user_app:update_schema', pk=column.schema.id)
