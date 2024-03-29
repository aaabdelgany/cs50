# Generated by Django 3.1.3 on 2021-02-06 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abduHR', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=10)),
                ('active', models.BooleanField()),
            ],
        ),
    ]
