# Generated by Django 3.2.4 on 2021-12-06 13:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_rename_location_groupjourney_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupJourneyCostType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GroupJourneyCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('price', models.IntegerField()),
                ('group_journey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.groupjourney')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.groupjourneycosttype')),
            ],
        ),
    ]