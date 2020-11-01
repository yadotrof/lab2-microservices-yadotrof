# Generated by Django 3.1.2 on 2020-11-01 17:11

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user_uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]