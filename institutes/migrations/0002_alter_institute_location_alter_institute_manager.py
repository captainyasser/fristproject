# Generated by Django 4.1.12 on 2025-02-20 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('institutes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='institute',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='institute',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='managed_institutes', to=settings.AUTH_USER_MODEL),
        ),
    ]
