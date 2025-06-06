# Generated by Django 5.2 on 2025-04-08 16:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('berberApp', '0002_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('barber', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='berberApp.barber')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='berberApp.service')),
            ],
            options={
                'unique_together': {('barber', 'date', 'time')},
            },
        ),
    ]
