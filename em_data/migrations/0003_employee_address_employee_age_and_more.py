# Generated by Django 4.1.12 on 2025-02-26 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0001_initial'),
        ('ranks', '0001_initial'),
        ('em_data', '0002_remove_employee_user_alter_employee_institute_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='alt_phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='amen_or_ola',
            field=models.BooleanField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='bus',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='employee',
            name='date_of_edara',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='date_of_retirement',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='dep_sort',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='departments.department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='district',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='food',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='employee',
            name='gender',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='governorate',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='health_status',
            field=models.CharField(blank=True, choices=[('جيدة', 'جيدة'), ('عمل إداري مكتبي', 'عمل إداري مكتبي'), ('ممنوع من حمل السلاح', 'ممنوع من حمل السلاح')], max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='id_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='image',
            field=models.ImageField(blank=True, default='employee_images/noimage.jpg', null=True, upload_to='employee_images/'),
        ),
        migrations.AddField(
            model_name='employee',
            name='mainornot',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='employee',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('أعزب', 'أعزب'), ('متزوج', 'متزوج'), ('مطلق', 'مطلق')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='nickname',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='operation',
            field=models.CharField(blank=True, choices=[('لم يحدد', 'لم يحدد'), ('السبت', 'السبت'), ('الأحد', 'الأحد'), ('الاثنين', 'الاثنين'), ('الثلاثاء', 'الثلاثاء'), ('الأربعاء', 'الأربعاء'), ('الخميس', 'الخميس'), ('الجمعة', 'الجمعة'), ('عمل يومي', 'عمل يومي'), ('انتداب', 'انتداب'), ('قرار66', 'قرار66')], default='لم يحدد', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='rahatcounter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='employee',
            name='rank_kind',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='tmamam',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='employee',
            name='total_leave',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='employee',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ranks.rank'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
