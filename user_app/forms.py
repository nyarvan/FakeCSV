from django import forms
from django.forms import inlineformset_factory
from .models import Schema, Column, Type


class SchemaForm(forms.ModelForm):
    COLUMN_SEPARATOR = [
        (',', 'Comma'),
        (';', 'Semicolon')
    ]

    STRING_CHARACTER = [
        ('\"', 'Double-quote'),
        ('\'', 'Quote')
    ]

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    column_separator = forms.ChoiceField(choices=COLUMN_SEPARATOR, widget=forms.Select(attrs={
        'class': 'form-select',
    }))
    string_character = forms.ChoiceField(choices=STRING_CHARACTER, widget=forms.Select(attrs={
        'class': 'form-select',
    }))

    class Meta:
        model = Schema
        fields = ['name', 'column_separator', 'string_character']


class ColumnForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    type = forms.ModelChoiceField(queryset=Type.objects.all(), empty_label='--------', widget=forms.Select(attrs={
        'class': 'form-select',
    }))
    from_range = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))
    to_range = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))
    order = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = Column
        fields = ['name', 'type', 'from_range', 'to_range', 'order']


ColumnFormSet = inlineformset_factory(
    Schema, Column, form=ColumnForm,
    extra=1, can_delete=True, can_delete_extra=True
)
