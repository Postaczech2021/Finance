# Generated by Django 5.1.2 on 2024-10-28 12:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0005_outcome_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outcome',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]