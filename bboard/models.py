# импортируем бузовый класс моделей django
from django.db import models

# Модель рубрика
class Rubric(models.Model):
    name = models.CharField(
        max_length=20, db_index=True, verbose_name='Название'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']
        
# Модель объявление
class Bb(models.Model):
    rubric = models.ForeignKey(
        Rubric, null=True, on_delete=models.PROTECT, verbose_name='Рубрика')
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликовано'
    )

    def __str__(self):
        return self.title

    class Meta:
        # Общее название того, что мы видим
        verbose_name_plural = 'Объявления'
        # Название конкретной записи
        verbose_name = 'Объявление'
        # как мы сортируем при просмотре в админке
        ordering = ['-published']