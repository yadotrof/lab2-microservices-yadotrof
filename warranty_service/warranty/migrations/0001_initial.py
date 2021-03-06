# Generated by Django 3.1.2 on 2020-11-01 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('status', models.CharField(choices=[('ON_WARRANTY', 'On warranty'), ('USE_WARRANTY', 'Use warranty'), ('REMOVED_FROM_WARRANTY', 'Removed from warranty')], max_length=25)),
                ('item_uuid', models.UUIDField(unique=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
