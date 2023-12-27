# Generated by Django 5.0 on 2023-12-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bboard', '0034_alter_bb_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bb',
            name='kind',
            field=models.CharField(blank=True, choices=[(None, 'Выберите тип публикации'), ('b', 'Куплю'), ('s', 'Продам'), ('c', 'Обменяю'), ('r', 'Rent')], default='Выберите тип публикации', max_length=1),
        ),
    ]
