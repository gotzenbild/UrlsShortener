# Generated by Django 2.2.6 on 2019-11-07 18:35

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urls',
            name='id',
        ),
        migrations.RemoveField(
            model_name='urls',
            name='short_url',
        ),
        migrations.AddField(
            model_name='urls',
            name='short_url_key',
            field=models.CharField(default=main.models.generate_key, max_length=6, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='urls',
            name='long_url',
            field=models.URLField(blank=True),
        ),
    ]
