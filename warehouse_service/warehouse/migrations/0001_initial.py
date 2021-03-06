# Generated by Django 3.1.2 on 2020-11-01 15:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_count', models.PositiveIntegerField(default=0)),
                ('model', models.CharField(default='', max_length=255)),
                ('size', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('canceled', models.BooleanField(default=False)),
                ('order_uuid', models.UUIDField(unique=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='warehouse.item')),
            ],
        ),
    ]
