# Generated by Django 5.0.1 on 2024-02-14 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0013_mpclsweight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionarie',
            name='riskscore',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]