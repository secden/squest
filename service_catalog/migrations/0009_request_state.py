# Generated by Django 3.1.7 on 2021-03-16 10:03

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0008_auto_20210316_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='state',
            field=django_fsm.FSMField(default='SUBMITTED', max_length=50),
        ),
    ]