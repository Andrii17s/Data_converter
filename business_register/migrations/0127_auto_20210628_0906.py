# Generated by Django 3.1.12 on 2021-06-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_register', '0126_auto_20210624_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='companysanction',
            name='initial_data',
            field=models.TextField(blank=True, default='', verbose_name='initial data'),
        ),
        migrations.AddField(
            model_name='countrysanction',
            name='initial_data',
            field=models.TextField(blank=True, default='', verbose_name='initial data'),
        ),
        migrations.AddField(
            model_name='personsanction',
            name='initial_data',
            field=models.TextField(blank=True, default='', verbose_name='initial data'),
        ),
    ]
