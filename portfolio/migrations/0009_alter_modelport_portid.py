# Generated by Django 5.0.1 on 2024-02-03 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_modelport_incept_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelport',
            name='portid',
            field=models.CharField(blank=True, null=True),
        ),
    ]