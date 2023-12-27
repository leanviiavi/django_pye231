# импортируем бузовый класс моделей django
from django.core.exceptions import ValidationError
from django.db import models
import uuid
import datetime

class MailExistsValidation:
    def __init__(self):
        self.mails : tuple = (
            "@gmail.com", "@gmail.ru",
            "@mail.ru", "@yandex.ru"
        )
    
    def __call__(self, context : str):
        for mail in self.mails:
            if mail in context:
                raise ValidationError(
                    '''
                    Описание объявления не может
                    иметь в себе почту.
                    ''',
                    code="mail_exception",
                    params={"mails" : self.mails, "current_mail" : mail},
                )


class RubricTitleValidation:
    def __init__(self):
        self.titles = (x.title for x in Bb.objects.all())
        self.names = (x.name for x in Rubric.objects.all())
    
    def __call__(self, context : str):
        if context in self.titles:
            raise ValidationError(
                '''
                Название рубрики не может совпадать
                с названием объявления.
                ''',
                code="title_title_exception",
                params={"titles" : self.titles},
            )
        # if context in self.titles:
        #     raise ValidationError(
        #         '''
        #         Название рубрики не может совпадать
        #         с названием существующей рубрики.
        #         ''',
        #         code="title_name_exception",
        #         params={"titles" : self.titles},
        #     )


class BboardPriceValidation:
    def __init__(self):
        self.max_price = 1_000_000_000
    
    def __call__(self, price : float):
        if price > self.max_price:
            raise ValidationError(
                f'''
                Цена больше чем {self.max_price}
                ''',
                code="too_big_price_exception",
                params={"max_price" : self.max_price}
            )

class BboardKindValidation:
    def __init__(self):
        self.max_count = 2
    
    def __call__(self, kind):
        self.kinds = Bb.objects.filter(kind = kind)
        if len(self.kinds) > self.max_count:
            raise ValidationError(
                '''
                Такого вида уже слишком много
                ''',
                code="too_much_count",
                params={"max_count" : self.max_count},
            )
        
# Модель рубрика
class Rubric(models.Model):
    def name_validation(title : str):
        return RubricTitleValidation()(context = title)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, 
                          editable=False)
    name = models.CharField(
        unique=True, help_text='Наименование рубрики', max_length=20, db_index=True, verbose_name='Название', validators = [name_validation]
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна ли рубрика?', blank=True)
    priority = models.DecimalField(default=0, verbose_name='Приоритет', max_digits=20, decimal_places=3)
    created_date = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    parent_rubric = models.ForeignKey('self', on_delete = models.PROTECT, default = None, null = True, blank = True)
    change_time = models.DateTimeField(auto_now = True, db_index = True, verbose_name = "Время изменения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['priority']


# Модель объявление
class Bb(models.Model):

    WORDS_TO_DELETE : tuple = (
        "Товар", "товар",
    )
    def mail_validation(stroke : str):
        return MailExistsValidation()(context = stroke)
    
    def price_validation(value : float):
        return BboardPriceValidation()(price = value)
    
    def kind_validation(value):
        return BboardKindValidation()(kind = value)
    
    def get_first_rubric(self):
        return Rubric.objects.get(name = self.rubric.name).parent_rubric
    
    def check_title(self):
        for word in Bb.WORDS_TO_DELETE:
            if word in self.title.lower():
                self.title = self.title.replace(word, "*"*len(word))
    
    @property
    def is_more_avg_price(self):
        bbs = list(Bb.objects.all())
        prices = [bb.price for bb in bbs]
        avg_price = sum(prices) / len(prices)
        return self.price > avg_price
    
    def title_and_price(self):
        """Наименование и цена в объявлении"""
        if self.price:
            return f"{self.title} : {self.price}"
        return f"{self.title}"
    
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
            print(f"Нельзя удалить, пока рубрика {self.rubric} активна")
    
    rubric = models.ForeignKey(
        Rubric, null=True, on_delete=models.SET(get_first_rubric), verbose_name='Рубрика')
    title = models.CharField(max_length=50, verbose_name='Товар', 
                             unique_for_date='published')
    content = models.TextField(null=True, blank=True, verbose_name='Описание', validators=[mail_validation])
    price = models.FloatField(null=True, blank=True, verbose_name='Цена', validators=[price_validation])

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
    kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.__empty__, blank=True, validators=[kind_validation])

    published = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликовано'
    )
    
    change_time = models.DateTimeField(auto_now = True, db_index = True, verbose_name = "Время изменения")

    def __str__(self):
        return self.title

    class Meta:
        indexes = [ 
            models.Index(fields = ["-published", "title"], name = "bb_main", condition = models.Q(price__lte = 10000)),
            models.Index(fields = ["title", "price", "rubric"]),
        ]
        # Общее название того, что мы видим
        verbose_name_plural = 'Объявления'
        # Название конкретной записи
        verbose_name = 'Объявление'
        # как мы сортируем при просмотре в админке
        ordering = ['rubric']
        # order_with_respect_to = "rubric"
        unique_together = ("title", "published")




"""

    Самостоятельная работа. 
    1. Добавить при создании BBoard пункт (Одобрено модератором), False - по умолчанию.
    2. Через админку предоставить возможность менять статус.
    3. Добавить возможность смотреть все BBoard что еще не прошли одобрение модератором.

"""






``