# Generated by Django 3.0.7 on 2020-07-22 13:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_ocean', '0004_auto_20200714_0751'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authority',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='register',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='taxpayertype',
            options={'ordering': ['id']},
        ),
    ]
