# Generated by Django 3.2.7 on 2021-09-08 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210902_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_note',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
