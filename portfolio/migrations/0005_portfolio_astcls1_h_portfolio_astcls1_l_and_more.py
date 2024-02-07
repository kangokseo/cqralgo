# Generated by Django 5.0.1 on 2024-02-03 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0004_portfolio_astcls5_h_portfolio_astcls5_l_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='astcls1_h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astcls1_l',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astcls2_h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astcls2_l',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astcls3_h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astcls3_l',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astcls4_h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astcls4_l',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astcls_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='astclsi_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='portid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='rskast_h',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='rskast_l',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='portfolio',
            name='rskdgr_h',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]