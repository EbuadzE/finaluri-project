# Generated by Django 5.1.7 on 2025-03-24 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='personal_number',
        ),
    ]
