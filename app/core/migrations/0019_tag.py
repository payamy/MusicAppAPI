# Generated by Django 3.1.2 on 2020-11-23 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20201113_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('title', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
    ]