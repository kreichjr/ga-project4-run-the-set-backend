# Generated by Django 3.2.9 on 2021-12-04 21:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0002_auto_20211204_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='createdAt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
