# Generated by Django 3.2 on 2021-08-18 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('store', 'store'), ('order', 'order'), ('ticket', 'ticket')], max_length=20),
        ),
    ]
