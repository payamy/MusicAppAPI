# Generated by Django 3.1.2 on 2020-11-27 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_advertisement_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='classroom',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.classroom'),
        ),
    ]
