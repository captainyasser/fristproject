# Generated by Django 4.1.12 on 2025-02-26 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='اسم الدرجة')),
            ],
            options={
                'verbose_name': 'الدرجة',
                'verbose_name_plural': 'الدرجات',
                'ordering': ['id'],
            },
        ),
    ]
