# Generated by Django 5.1.3 on 2025-01-06 16:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0009_alter_departments_location_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departments',
            name='doctor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='hospital.doctor'),
            preserve_default=False,
        ),
    ]
