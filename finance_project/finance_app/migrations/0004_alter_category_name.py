# Generated by Django 5.1.2 on 2024-10-26 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance_app', '0003_category_is_income'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(default=1, max_length=100, unique=True),
        ),
    ]
