# Generated by Django 4.0.3 on 2022-04-29 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buddiesforstudies', '0015_location_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='time',
            field=models.TimeField(null=b'I01\n'),
            preserve_default=b'I01\n',
        ),
    ]