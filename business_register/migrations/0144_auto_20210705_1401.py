# Generated by Django 3.1.12 on 2021-07-05 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business_register', '0143_auto_20210705_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaries', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='corporaterights',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='corporate_rights', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='corporaterightsright',
            name='corporate_rights',
            field=models.ForeignKey(help_text='right to corporate rights', on_delete=django.db.models.deletion.CASCADE, related_name='rights', to='business_register.corporaterights', verbose_name='corporate rights right'),
        ),
        migrations.AlterField(
            model_name='income',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incomes', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='liability',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liabilities', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='luxuryitem',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='luxuries', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='luxuryitemright',
            name='luxury_item',
            field=models.ForeignKey(help_text='right to the luxury item', on_delete=django.db.models.deletion.CASCADE, related_name='rights', to='business_register.luxuryitem', verbose_name='luxury_item_right'),
        ),
        migrations.AlterField(
            model_name='money',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='money', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='ngoparticipation',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ngo_participation', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='parttimejob',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='part_time_jobs', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='property',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='propertyright',
            name='property',
            field=models.ForeignKey(help_text='right to the property', on_delete=django.db.models.deletion.CASCADE, related_name='rights', to='business_register.property', verbose_name='property_right'),
        ),
        migrations.AlterField(
            model_name='securities',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='securities', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='securitiesright',
            name='securities',
            field=models.ForeignKey(help_text='right to securities', on_delete=django.db.models.deletion.CASCADE, related_name='rights', to='business_register.securities', verbose_name='securities_right'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='declaration',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='business_register.declaration', verbose_name='declaration'),
        ),
        migrations.AlterField(
            model_name='vehicleright',
            name='car',
            field=models.ForeignKey(help_text='right to the vehicle', on_delete=django.db.models.deletion.CASCADE, related_name='rights', to='business_register.vehicle', verbose_name='vehicle_right'),
        ),
    ]
