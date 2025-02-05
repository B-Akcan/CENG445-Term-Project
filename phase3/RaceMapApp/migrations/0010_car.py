# Generated by Django 5.1.4 on 2024-12-17 08:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RaceMapApp', '0009_alter_component_rotation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('model', models.CharField(max_length=20, unique=True)),
                ('driver', models.CharField(max_length=20)),
                ('topspeed', models.FloatField()),
                ('topfuel', models.FloatField()),
                ('map', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RaceMapApp.map')),
            ],
        ),
    ]
