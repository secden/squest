# Generated by Django 3.1.7 on 2021-07-27 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_catalog', '0006_auto_20210723_2149'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceStateHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('extra_vars', models.JSONField(default=dict)),
                ('instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instances', related_query_name='instance', to='service_catalog.service')),
                ('job_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_catalog.jobtemplate')),
            ],
        ),
        migrations.CreateModel(
            name='GlobalHook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('model', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('extra_vars', models.JSONField(default=dict)),
                ('job_template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='service_catalog.jobtemplate')),
            ],
        ),
    ]