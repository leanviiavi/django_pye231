# Generated by Django 5.0 on 2023-12-20 14:10

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0013_alter_rubric_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rubric',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
