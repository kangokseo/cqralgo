# Generated by Django 5.0.1 on 2024-02-12 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0011_dailympweight_delete_dailympwt'),
    ]

    operations = [
        migrations.CreateModel(
            name='monthlyMPvalue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('port_id', models.CharField(blank=True, null=True)),
                ('item1_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('item2_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('item3_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('item4_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('item5_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('item6_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('item7_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('item8_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('port_val', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
                ('port_ret', models.DecimalField(blank=True, decimal_places=6, max_digits=20, null=True)),
            ],
        ),
    ]
