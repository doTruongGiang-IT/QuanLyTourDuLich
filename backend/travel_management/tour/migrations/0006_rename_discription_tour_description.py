# Generated by Django 3.2.4 on 2021-12-04 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0005_tour_discription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tour',
            old_name='discription',
            new_name='description',
        ),
    ]
