# Generated by Django 5.0.1 on 2024-02-12 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0012_monthlympvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='MPclsweight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('port_id', models.CharField(blank=True, null=True)),
                ('cls5_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('cls4_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('cls3_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('cls2_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('cls1_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('risk_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
            ],
        ),
    ]