# Generated by Django 3.1.3 on 2021-02-04 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0010_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='num_likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
