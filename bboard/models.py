# импортируем бузовый класс моделей django
from django.core.exceptions import ValidationError
from django.db import models
import uuid


class MailExistsValidation:
    def __init__(self):
        self.mails: tuple = (
            '@gmail.com', '@gmail.ru',
            '@mail.ru', '@yandex.ru'
        )

    def __call__(self, context: str):
        for mail in self.mails:
            if mail in context:
                raise ValidationError(
                    '''
                    Описание обьявления не может иметь в себе почту
                    ''',
                    code='mail_exception',
                    params={'mails' : self.mails, 'current_mail' : mail}
                )


class RubricValidation:
    def __init__(self):
        self.rubrics = Rubric.objects.all()
        self.title = [rubric.name for rubric in self.rubrics]

    def __call__(self, context: str):
        if len(context) > 15:
            raise ValidationError(
                '''
                Название рубрики не может превышать 14 символов
                ''',
                code='title_more_exception',
                params={'titles' : self.titles, 'current_title' : context}
            )

        if len(context) < 5:
            raise ValidationError(
                '''
                Название рубрики не может быть меньше 5 символов
                ''',
                code='title_less_exception',
                params={'titles' : self.titles, 'current_title' : context}
            ) 


class BboardValidation:
    def __init__(self):
        self.bbs = Bb.objects.all()
        self.prices = [bb.price for bb in self.bbs]

    def __call__(self, context: int):
        for price in self.prices:
            if context > 10000:
                raise ValidationError(
                    '''
                    Цена не может превышать 10000 тенге
                    '''
                )
            if context < 100:
                raise ValidationError(
                    '''
                    Цена не может быть ниже 100 тенге
                    '''
                )

# Модель рубрика
class Rubric(models.Model):

    def rubric_title_validation(stroke: str):
        return RubricValidation()(context=stroke)

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, 
                          editable=False)
    name = models.CharField(
        unique=True, help_text='Наименование рубрики', max_length=20, db_index=True, verbose_name='Название', validators=[rubric_title_validation]
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна ли рубрика?', blank=True)
    priority = models.DecimalField(default=0, verbose_name='Приоритет', max_digits=20, decimal_places=3)
    created_date = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    parent_rubric = models.ForeignKey('self', on_delete=models.PROTECT, default=None, blank=True, null=True)
    updated_date = models.DateTimeField(verbose_name="Изменено", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['priority']

    
   


# Модель объявление
class Bb(models.Model):

    WORDS_TO_DELETE: tuple = (
        'Товар', 'товар', ''
    )

    def bb_price_validation(number: float):
        return BboardValidation()(context=number)

    def mail_validation(stroke: str):
        return MailExistsValidation()(context=stroke)

    def get_first_rubric(self):
        return Rubric.objects.get(name=self.rubric.name).parent_rubric
    
    def check_title(self):
        for word in Bb.WORDS_TO_DELETE:
            if word in self.title.lower():
                self.title = self.title.replace(word, '*'*len(word))

    @property
    def is_more_avg_price(self):
        bbs = list(Bb.objects.all())
        prices = [bb.price for bb in bbs]
        _avg_price = sum(prices) / len(prices)
        return self.price > _avg_price

    def title_and_price(self):
        "Наименование и цена в обьявлений"
        if self.price:
            return f'{self.title} : {self.price}'
        return self.title


    def save(self, *args, **kwargs):
        print(args, kwargs)

        # if self.is_model_correct():
        #     self.check_title()
        #     super().save(*args, **kwargs)

        self.check_title()
        super().save(*args, **kwargs)        

    def delete(self, *args, **kwargs):
        if not self.rubric.is_active:
            super().delete(*args, **kwargs)
        else:
            print(f'Нельзя удалить, пока рубрика {self.rubric} активна')


    rubric = models.ForeignKey(
        Rubric, null=True, on_delete=models.SET(get_first_rubric), verbose_name='Рубрика')
    title = models.CharField(max_length=50, verbose_name='Товар', 
                             unique_for_date='published')
    content = models.TextField(null=True, blank=True, verbose_name='Описание', validators=[mail_validation])
    price = models.FloatField(null=True, blank=True, verbose_name='Цена', validators=[bb_price_validation   ])

    class Kinds(models.TextChoices):
        BUY = 'b', 'Куплю'
        SELL = 's', 'Продам'
        EXCENGE = 'c', 'Обменяю'
        RENT = 'r'
        __empty__ = 'Выберите тип публикации'

    kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.__empty__, blank=True)

    published = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликовано'
    )

    def __str__(self):
        return self.title

    class Meta:
        indexes: list = [
            models.Index(fields=['-published', 'title'],
                         name='bb_main',
                         condition=models.Q(price__lte=10000)),
            models.Index(fields=['title', 'price', 'rubric']),
        ]
        # Общее название того, что мы видим
        verbose_name_plural = 'Объявления'
        # Название конкретной записи
        verbose_name = 'Объявление'
        # как мы сортируем при просмотре в админке
        # ordering = ['-published']
        order_with_respect_to = 'rubric'
        unique_together = ('title', 'published')


"""

    Самостоятельная работа. 
    1. Добавить при создании BBoard пункт (Одобрено модератором), False - по умолчанию.
    2. Через админку предоставить возможность менять статус.
    3. Добавить возможность смотреть все BBoard что еще не прошли одобрение модератором.

"""






