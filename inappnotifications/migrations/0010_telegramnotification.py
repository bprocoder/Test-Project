# Generated by Django 3.2.4 on 2023-09-09 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inappnotifications', '0009_notification_slotnotisendstatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_id', models.CharField(max_length=255)),
                ('user_id', models.CharField(max_length=255)),
            ],
        ),
    ]