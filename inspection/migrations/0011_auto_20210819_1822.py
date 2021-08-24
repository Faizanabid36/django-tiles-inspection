# Generated by Django 3.1.6 on 2021-08-19 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inspection', '0010_auto_20210819_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspectionmodel',
            name='user_inspection_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='reportmodel',
            name='user_inspection_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.CreateModel(
            name='UserInspectionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='null', max_length=255)),
                ('generate_report', models.BooleanField(default=False)),
                ('inspection_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.inspectionmodel')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inspection.employeemodel')),
            ],
        ),
    ]