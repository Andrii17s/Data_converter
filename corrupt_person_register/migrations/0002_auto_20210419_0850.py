# Generated by Django 3.1.8 on 2021-04-19 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corrupt_person_register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorruptIndividual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the object was created. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='When the object was update. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.', null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('person_id', models.PositiveIntegerField(help_text='identifier of the person in the NAZK database.', verbose_name='the NAZK identifier of person')),
                ('punishment_type', models.CharField(choices=[('CD', 'Court decision'), ('DA', 'Disciplinary action')], help_text="Punishment type. Can be 'Court decision' or 'Disciplinary action'.", max_length=2, verbose_name='punishment type')),
                ('offense_id', models.PositiveIntegerField(blank=True, help_text='Identifier of the corruption offense.', null=True, verbose_name='the NAZK identifier of offense')),
                ('offense_name', models.TextField(blank=True, default='', help_text='The name of the composition of the corruption offense / Method of imposing a disciplinary process.', verbose_name='the name of offense')),
                ('punishment', models.TextField(blank=True, default='', help_text='The essence of satisfaction of claims / Type of disciplinary action.', verbose_name='punishment')),
                ('decree_date', models.DateField(blank=True, help_text='Date in YYYY-MM-DD format. Date of the order on imposition of disciplinary sanction.', null=True, verbose_name='decree date')),
                ('decree_number', models.CharField(blank=True, default='', help_text='The number of the order imposing a disciplinary sanction.', max_length=100, verbose_name='decree number')),
                ('court_case_number', models.CharField(blank=True, default='', help_text='The number of court case.', max_length=100, verbose_name='court case number')),
                ('sentence_date', models.DateField(blank=True, help_text='Date in YYYY-MM-DD format. Date of court decision.', null=True, verbose_name='sentence date')),
                ('sentence_number', models.CharField(blank=True, default='', help_text='The number of court decision.', max_length=100, verbose_name='sentence number')),
                ('punishment_start', models.DateField(blank=True, help_text='Date in YYYY-MM-DD format. Date of entry into force of the court decision.', null=True, verbose_name='punishment start')),
                ('court_id', models.PositiveIntegerField(blank=True, help_text='Identifier of court.', null=True, verbose_name='the NAZK identifier of court')),
                ('court_name', models.CharField(blank=True, default='', help_text='The name of the court.', max_length=500, verbose_name='the name of court')),
                ('last_name', models.CharField(blank=True, db_index=True, default='', help_text='The last name of the individual at the time of the offense.', max_length=50, verbose_name='last name')),
                ('first_name', models.CharField(blank=True, db_index=True, default='', help_text='The name of the individual at the time of the offense.', max_length=50, verbose_name='first name')),
                ('middle_name', models.CharField(blank=True, db_index=True, default='', help_text='The middle name of the individual at the time of the offense.', max_length=50, verbose_name='middle name')),
                ('place_of_work', models.CharField(blank=True, default='', help_text='Place of work of an individual at the time of the offense.', max_length=500, verbose_name='place of work')),
                ('occupation', models.CharField(blank=True, default='', help_text='Position of an  individual at the time of the offense.', max_length=500, verbose_name='occupation')),
                ('activity_sphere_id', models.PositiveIntegerField(blank=True, help_text='Identifier of the sphere of activity of an individual at the time of the offense', null=True, verbose_name='the NAZK identifier of activity sphere')),
                ('activity_sphere_name', models.CharField(blank=True, default='', help_text='Name of the sphere of activity of an  individual at the time of the offense.', max_length=500, verbose_name='the name of activity sphere')),
                ('codex_articles', models.ManyToManyField(help_text='The article under which the person was prosecuted.', to='corrupt_person_register.CorruptCodexArticle', verbose_name='codex articles')),
            ],
            options={
                'verbose_name': 'Individual who have committed corruption or corruption-related offenses',
            },
        ),
        migrations.CreateModel(
            name='CorruptLegalEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='When the object was created. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='When the object was update. In YYYY-MM-DDTHH:mm:ss.SSSSSSZ format.', null=True)),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, default=None, editable=False, null=True)),
                ('person_id', models.PositiveIntegerField(help_text='identifier of the person in the NAZK database.', verbose_name='the NAZK identifier of person')),
                ('punishment_type', models.CharField(choices=[('CD', 'Court decision'), ('DA', 'Disciplinary action')], help_text="Punishment type. Can be 'Court decision' or 'Disciplinary action'.", max_length=2, verbose_name='punishment type')),
                ('offense_id', models.PositiveIntegerField(blank=True, help_text='Identifier of the corruption offense.', null=True, verbose_name='the NAZK identifier of offense')),
                ('offense_name', models.TextField(blank=True, default='', help_text='The name of the composition of the corruption offense / Method of imposing a disciplinary process.', verbose_name='the name of offense')),
                ('punishment', models.TextField(blank=True, default='', help_text='The essence of satisfaction of claims / Type of disciplinary action.', verbose_name='punishment')),
                ('decree_date', models.DateField(blank=True, help_text='Date in YYYY-MM-DD format. Date of the order on imposition of disciplinary sanction.', null=True, verbose_name='decree date')),
                ('decree_number', models.CharField(blank=True, default='', help_text='The number of the order imposing a disciplinary sanction.', max_length=100, verbose_name='decree number')),
                ('court_case_number', models.CharField(blank=True, default='', help_text='The number of court case.', max_length=100, verbose_name='court case number')),
                ('sentence_date', models.DateField(blank=True, help_text='Date in YYYY-MM-DD format. Date of court decision.', null=True, verbose_name='sentence date')),
                ('sentence_number', models.CharField(blank=True, default='', help_text='The number of court decision.', max_length=100, verbose_name='sentence number')),
                ('punishment_start', models.DateField(blank=True, help_text='Date in YYYY-MM-DD format. Date of entry into force of the court decision.', null=True, verbose_name='punishment start')),
                ('court_id', models.PositiveIntegerField(blank=True, help_text='Identifier of court.', null=True, verbose_name='the NAZK identifier of court')),
                ('court_name', models.CharField(blank=True, default='', help_text='The name of the court.', max_length=500, verbose_name='the name of court')),
                ('addr_post_index', models.CharField(blank=True, default='', help_text='Address of registration of a legal entity at the time of the offense: postal code.', max_length=50, verbose_name='postcode')),
                ('addr_country_id', models.PositiveIntegerField(blank=True, help_text='Address of registration of a legal entity at the time of law enforcement: country identifier.', null=True, verbose_name='the NAZK identifier of country')),
                ('addr_country_name', models.CharField(blank=True, default='', help_text='Address of registration of a legal entity at the time of the offense: name of the country.', max_length=100, verbose_name='country')),
                ('addr_state_id', models.PositiveIntegerField(blank=True, help_text='The address of registration of the legal entity at the time of the offense: the identifier of the region/city of national importance.', null=True, verbose_name='the identifier of the region/city')),
                ('addr_state_name', models.CharField(blank=True, default='', help_text='The address of registration of the legal entity at the time of the offense: the name of the region/city of national importance', max_length=100, verbose_name='the name of the region/city')),
                ('addr_str', models.CharField(blank=True, default='', help_text='The address of registration of the legal entity at the time of the offense: district, town, street, house, premises in the form of a line.', max_length=300, verbose_name='full address')),
                ('short_name', models.CharField(blank=True, db_index=True, default='', help_text='Abbreviated name of the legal entity at the time of the offense.', max_length=100, verbose_name='short name of the legal entity')),
                ('legal_entity_name', models.CharField(blank=True, db_index=True, default='', help_text='The name of the legal entity at the time of the offense.', max_length=500, verbose_name='the name of the legal entity')),
                ('registration_number', models.CharField(blank=True, db_index=True, default='', help_text='EDRPOU code of the legal entity.', max_length=100, verbose_name='EDRPOU')),
                ('legal_form_id', models.PositiveIntegerField(blank=True, default='', help_text='Identifier of organizational and legal form of ownership of a legal entity.', verbose_name='the NAZK identifier of legal form')),
                ('legal_form_name', models.CharField(blank=True, default='', help_text='The name of the organizational and legal form of ownership of the legal entity.', max_length=500, verbose_name='the name of legal form')),
                ('codex_articles', models.ManyToManyField(help_text='The article under which the person was prosecuted.', to='corrupt_person_register.CorruptCodexArticle', verbose_name='codex articles')),
            ],
            options={
                'verbose_name': 'Legal entity who have committed corruption or corruption-related offenses',
            },
        ),
        migrations.RemoveField(
            model_name='corruptperson',
            name='activity_sphere',
        ),
        migrations.RemoveField(
            model_name='corruptperson',
            name='codex_articles',
        ),
        migrations.RemoveField(
            model_name='corruptperson',
            name='court',
        ),
        migrations.RemoveField(
            model_name='corruptperson',
            name='legal_form',
        ),
        migrations.RemoveField(
            model_name='corruptperson',
            name='offense',
        ),
        migrations.DeleteModel(
            name='ActivityShpere',
        ),
        migrations.DeleteModel(
            name='CorruptPerson',
        ),
        migrations.DeleteModel(
            name='Court',
        ),
        migrations.DeleteModel(
            name='LegalForm',
        ),
        migrations.DeleteModel(
            name='Offense',
        ),
    ]
