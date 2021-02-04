# Generated by Django 3.1.2 on 2021-02-01 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20201210_2246'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('title', models.CharField(max_length=255, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='advertisement',
            name='categories',
            field=models.ManyToManyField(to='core.Category'),
        ),
    ]