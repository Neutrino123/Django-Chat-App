# Generated by Django 4.1.13 on 2024-05-07 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_profile_created_alter_profile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='username',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
