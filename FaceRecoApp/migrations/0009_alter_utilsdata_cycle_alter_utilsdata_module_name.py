# Generated by Django 5.0.3 on 2024-04-13 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FaceRecoApp', '0008_alter_utilsdata_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilsdata',
            name='cycle',
            field=models.CharField(choices=[('cycle_preparatoire', 'Preparatory Cycle'), ('cycle_ingenieur', 'Engineering Cycle')], db_column='cycle', max_length=80),
        ),
        migrations.AlterField(
            model_name='utilsdata',
            name='module_name',
            field=models.CharField(choices=[(None, '')], db_column='module', max_length=400),
        ),
    ]
