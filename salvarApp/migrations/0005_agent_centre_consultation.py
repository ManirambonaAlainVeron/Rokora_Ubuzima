# Generated by Django 2.0 on 2020-04-22 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('salvarApp', '0004_auto_20200422_2037'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent_centre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_sanitaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salvarApp.Agent_sanitaire')),
                ('centre_sanitaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salvarApp.Centre_sanitaire')),
            ],
            options={
                'db_table': 'Agent_centre',
            },
        ),
        migrations.CreateModel(
            name='Consultation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('traitement', models.TextField()),
                ('agent_centre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salvarApp.Agent_centre')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salvarApp.Patient')),
            ],
            options={
                'db_table': 'Consultation',
            },
        ),
    ]