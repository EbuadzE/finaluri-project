# Generated by Django 5.1.7 on 2025-03-16 13:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newapp', '0003_remove_mycars_date_mycars_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='mycars',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mycars',
            name='description',
            field=models.TextField(default='No description'),
        ),
        migrations.AddField(
            model_name='mycars',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='cars'),
        ),
        migrations.AddField(
            model_name='mycars',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
