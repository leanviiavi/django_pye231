# Generated by Django 5.0 on 2023-12-25 14:36

import bboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0030_alter_bb_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='content',
            field=models.TextField(blank=True, null=True, validators=[bboard.models.Bb.mail_validation], verbose_name='Описание'),
        ),
    ]
