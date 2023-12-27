# импортируем бузовый класс моделей django
from django.core.exceptions import ValidationError
from django.db import models
import uuid


class MailExistsValidation:
    def __init__(self):
        self.mails: tuple = (
            '@gmail.com', '@gmail.ru',
            '@mail.ru', '@yandex.ru',
        )


    def __call__(self, context: str):
        for mail in self.mails:
            if mail in context:
                raise ValidationError(
                    '''
                    Описание объявления не может
                    иметь в себе почту.
                    ''',
                    code='mail_exception',
                    params={'mails': self.mails, 'current_mail': mail}
                )


# Модель рубрика
class Rubric(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
                          editable=False)
    name = models.CharField(
        unique=True, help_text='Наименование рубрики', max_length=20, db_index=True, verbose_name='Название'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна ли рубрика?', blank=True)
    priority = models.DecimalField(default=0, verbose_name='Приоритет', max_digits=20, decimal_places=3)
    created_date = models.DateTimeField(verbose_name='Создано', auto_now_add=True)

    parent_rubric = models.ForeignKey('self', on_delete=models.PROTECT, null=True, default=None, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['priority']


# Модель объявление
class Bb(models.Model):

    WORDS_TO_DELETE: tuple = (
        'Товар', 'товар',
    )

    def mail_validation(stroke: str):
        return MailExistsValidation()(context=stroke)

    """ метод выдает первую рубрику из списка всех"""
    def get_first_rubric():
        return Rubric.objects.first()
    
    """ метод удаляет WORDS_TO_DELETE с Наименования объявления"""
    def check_title(self):
        for word in Bb.WORDS_TO_DELETE:
            if word in self.title:
                self.title = self.title.replace(word, '*'*len(word))

    
    @property
    def is_more_avg_price(self):
        """отмечает стилем если цена выше средней"""
        bbs = list(Bb.objects.all())
        prices = [bb.price for bb in bbs]
        _avg_price = sum(prices) / len(prices)
        return "background-color: red;" if self.price > _avg_price else ""
        

    """ метод выдает шаблон (Наименование : Цена)"""
    @property
    def title_and_price(self):
        """Наименование и цена в объявлении"""
        if self.price:
            return f'{self.title} : {self.price}'
        return self.title
    
    # title_and_price.short_description = 'Наименование и цена в объявлении'

    """ встроенный метод, который отрабатывает при ихменениях, добавлениях"""
    def save(self, *args, **kwargs):
        print(args, kwargs)
        """
        проверяет модель на корректность 
            if self.is_model_correct():
                self.check_title()
                super().save(*args, **kwargs)
        """
        self.check_title()
        super().save(*args, **kwargs)

    """ встроенный метод вызываемый при удалении модели """
    def delete(self, *args, **kwargs):
        if not self.rubric.is_active:
            super().delete(*args, **kwargs)
        else:
            print(f'Нельзя удалить, пока рубрика {self.rubric} активна')




    rubric = models.ForeignKey(
        Rubric, null=True, on_delete=models.CASCADE, verbose_name='Рубрика')
    title = models.CharField(max_length=50, verbose_name='Товар', 
                             unique_for_date='published')
    content = models.TextField(null=True, blank=True, verbose_name='Описание', validators=[mail_validation])
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')

    class Kinds(models.TextChoices):
        BUY = 'b', 'Куплю'
        SELL = 's', 'Продам'
        EXCENGE = 'c', 'Обменяю'
        RENT = 'r'
        __empty__ = 'Выберите тип публикации'
    # KINDS = (
    #     (None, "Выберите тип публикации"),
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )
    kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.__empty__, blank=True)

    published = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликовано'
    )

    def __str__(self):
        return self.title

    class Meta:
        # indexes = [
        #     models.Index(fields=['-published', 'title'],
        #                  name='bb_main',
        #                  condition=models.Q(price__lte=10000)),
        #     models.Index(fields=['title', 'price', 'rubric']),
        # ]
        # Общее название того, что мы видим
        verbose_name_plural = 'Объявления'
        # Название конкретной записи
        verbose_name = 'Объявление'
        # как мы сортируем при просмотре в админке
        ordering = ['rubric']
        # order_with_respect_to = 'rubric'
        unique_together = ('title', 'published')







"""


    Создать валидаторы на: Rubric - валидация наименования,
                           Bboard - валидация price, kind


"""


