# Generated by Django 3.1.2 on 2020-10-23 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20201023_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='biography',
            field=models.CharField(default='no information', max_length=255),
        ),
    ]
