# Generated by Django 3.0.7 on 2021-03-05 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_ocean', '0021_auto_20210305_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authority',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the object was created. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.'),
        ),
        migrations.AlterField(
            model_name='authority',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='When the object was update. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.', null=True),
        ),
        migrations.AlterField(
            model_name='register',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the object was created. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.'),
        ),
        migrations.AlterField(
            model_name='register',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='When the object was update. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.', null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the object was created. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.'),
        ),
        migrations.AlterField(
            model_name='status',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='When the object was update. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.', null=True),
        ),
        migrations.AlterField(
            model_name='taxpayertype',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the object was created. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.'),
        ),
        migrations.AlterField(
            model_name='taxpayertype',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='When the object was update. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.', null=True),
        ),
    ]
