# Generated by Django 5.1.1 on 2024-09-12 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_portfolio_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfolio',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='portfolio',
            name='total_value',
        ),
        migrations.AlterField(
            model_name='portfolio',
            name='stocks',
            field=models.JSONField(default=dict),
        ),
    ]
