# Generated by Django 4.0.6 on 2023-03-11 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.TextField(default='virtual', max_length=150),
        ),
        migrations.AlterField(
            model_name='event',
            name='link',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]
