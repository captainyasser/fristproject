# Generated by Django 4.1.12 on 2025-02-20 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutes', '0003_remove_institute_manager_alter_institute_location_and_more'),
        ('em_data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user',
        ),
        migrations.AlterField(
            model_name='employee',
            name='institute',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='institutes.institute'),
        ),
        migrations.DeleteModel(
            name='Institute',
        ),
    ]
