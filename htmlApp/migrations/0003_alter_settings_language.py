# Generated by Django 5.0.4 on 2024-07-25 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('htmlApp', '0002_rename_user_id_settings_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userProfile',
            name='language',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
