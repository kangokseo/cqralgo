# Generated by Django 5.0.1 on 2024-03-07 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0017_monthlympvalue_acum_ret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailympvalue',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dailympweight',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='monthlympvalue',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mpclsweight',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
