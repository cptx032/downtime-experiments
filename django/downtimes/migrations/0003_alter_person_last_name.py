# Generated by Django 3.2.6 on 2021-08-12 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downtimes', '0002_person_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(max_length=512),
        ),
    ]