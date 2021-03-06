# Generated by Django 2.0 on 2020-04-22 17:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('salvarApp', '0003_auto_20200422_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent_sanitaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('profil', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='agent_centre',
            name='centre_sanitaire',
        ),
        migrations.RemoveField(
            model_name='consultation',
            name='agent_centre',
        ),
        migrations.RemoveField(
            model_name='consultation',
            name='patient',
        ),
        migrations.DeleteModel(
            name='Agent_centre',
        ),
        migrations.DeleteModel(
            name='Consultation',
        ),
    ]
