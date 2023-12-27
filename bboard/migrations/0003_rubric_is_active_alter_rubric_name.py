# Generated by Django 5.0 on 2023-12-20 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0002_rubric_alter_bb_options_alter_bb_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubric',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='rubric',
            name='name',
            field=models.CharField(db_index=True, help_text='Наименование рубрики', max_length=20, verbose_name='Название'),
        ),
    ]
