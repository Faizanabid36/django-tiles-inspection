# Generated by Django 3.1.6 on 2021-08-19 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0014_auto_20210819_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinspectionmodel',
            name='report_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='inspection.reportmodel'),
        ),
    ]
