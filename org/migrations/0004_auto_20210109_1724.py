# Generated by Django 3.1.1 on 2021-01-09 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('org', '0003_auto_20210109_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='target_amount',
            field=models.IntegerField(blank=True, default=0.0, null=True),
        ),
    ]