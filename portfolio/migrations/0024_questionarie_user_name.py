# Generated by Django 5.0.1 on 2024-05-05 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0023_profile_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionarie',
            name='user_name',
            field=models.CharField(blank=True, null=True),
        ),
    ]