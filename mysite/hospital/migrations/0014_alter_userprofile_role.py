# Generated by Django 5.1.3 on 2025-01-07 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0013_warnings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('doctor', 'doctor'), ('patient', 'patient')], max_length=15),
        ),
    ]
