# Generated by Django 3.2.7 on 2021-09-20 22:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('employee_app', '0002_auto_20210916_2245'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAttendanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_time', models.DateTimeField(blank=True, null=True)),
                ('out_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.BooleanField(default=False)),
                ('employees', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
