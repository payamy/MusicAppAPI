# Generated by Django 3.1.2 on 2021-02-04 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20210204_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='compatibility',
            field=models.IntegerField(default=0),
        ),
    ]
