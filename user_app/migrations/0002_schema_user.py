# Generated by Django 4.1.5 on 2023-01-30 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='schema',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
            preserve_default=False,
        ),
    ]