# Generated by Django 3.1.6 on 2021-08-19 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0012_remove_userinspectionmodel_inspection_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinspectionmodel',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
