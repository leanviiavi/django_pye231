# Generated by Django 5.0 on 2023-12-21 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0028_alter_rubric_changed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='changed',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Изменено'),
        ),
    ]
