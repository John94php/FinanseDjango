# Generated by Django 5.0.4 on 2024-05-18 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FinanseDjango', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='expense_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='income',
            old_name='income_date',
            new_name='date',
        ),
    ]
