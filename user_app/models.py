from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Type(models.Model):
    name = models.CharField(max_length=15, verbose_name='Name')
    from_range = models.BooleanField(default=False, verbose_name='View range: From')
    to_range = models.BooleanField(default=False, verbose_name='View range: To')

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Column(models.Model):
    name = models.CharField(max_length=15, verbose_name='Name')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type', verbose_name='Type')
    schema = models.ForeignKey('Schema', on_delete=models.CASCADE, verbose_name='Schema')
    from_range = models.IntegerField(null=True, blank=True, verbose_name='Range: From')
    to_range = models.IntegerField(null=True, blank=True, verbose_name='Range: To')
    order = models.IntegerField(verbose_name='Order')

    class Meta:
        ordering = ('order', )

    def __str__(self):
        return self.name


class Schema(models.Model):
    COLUMN_SEPARATOR = [
        (',', 'Comma'),
        (';', 'Semicolon')
    ]

    STRING_CHARACTER = [
        ('\"', 'Double-quote'),
        ('\'', 'Quote')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True, verbose_name='User')
    name = models.CharField(max_length=25, verbose_name='Name')
    column_separator = models.CharField(max_length=1, choices=COLUMN_SEPARATOR, verbose_name='Column separator')
    string_character = models.CharField(max_length=1, choices=STRING_CHARACTER, verbose_name='String character')
    modified = models.DateTimeField(auto_now=True, verbose_name='Modified')
    
    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name


class FileCSV(models.Model):
    def upload_file(instance, filename):
        _now = datetime.now()

        return f'{instance.user.username}/{_now.year}/{_now.month}/{_now.day}/{filename}'


    schema = models.ForeignKey(Schema, on_delete=models.CASCADE, verbose_name='Schema')
    status = models.BooleanField(default=False, verbose_name='Status')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    file = models.FileField(upload_to=upload_file, verbose_name='File')

    class Meta:
        ordering = ('status', )

    def __str__(self):
        return f'{self.created} - {self.schema}'
