# Generated by Django 5.0 on 2023-12-20 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0005_alter_bb_title_alter_rubric_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rubric',
            options={'ordering': ['priority'], 'verbose_name': 'Рубрика', 'verbose_name_plural': 'Рубрики'},
        ),
        migrations.AddField(
            model_name='rubric',
            name='priority',
            field=models.SmallIntegerField(default=0, verbose_name='Приоритет'),
        ),
    ]
