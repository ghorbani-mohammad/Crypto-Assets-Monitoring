# Generated by Django 5.0 on 2023-12-31 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0009_alter_notification_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='market',
            field=models.CharField(blank=True, choices=[('irt', 'irt'), ('usdt', 'usdt')], max_length=10, null=True),
        ),
    ]
