# Generated by Django 3.0.1 on 2020-02-21 16:10

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('dateStart', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('dateEnd', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('eventType', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='events.type')),
            ],
        ),
    ]