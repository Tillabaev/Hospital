# Generated by Django 5.1.3 on 2025-01-06 16:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_remove_doctor_specialty_doctor_specialty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='departments',
            name='doctor',
        ),
        migrations.AddField(
            model_name='departments',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='hospital.doctor'),
        ),
    ]
