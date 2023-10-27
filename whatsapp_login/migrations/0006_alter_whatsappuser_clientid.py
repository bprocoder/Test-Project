# Generated by Django 3.2.4 on 2023-09-21 11:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('whatsapp_login', '0005_whatsappuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whatsappuser',
            name='clientid',
            field=models.OneToOneField(db_column='clientid', on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]