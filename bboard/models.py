# импортируем бузовый класс моделей django
from typing import Any
from django.core.exceptions import ValidationError
from django.db import models
import uuid


class KindValidation:
    def __init__(self):
        ...


    def __call__(self, kind: str):
        if len(kind) != 1:
                raise ValidationError(
                    'Incorrect kind chosen',
                    code="kind exception",
                    params={"kinds":(),"current_kind":kind}
                )

class PriceValidation:
    def __init__(self):
        self.prices:tuple = (
            
        )


    def __call__(self, price: int):
        if price < 0 or price > 1000000000 or price is None:
                raise ValidationError(
                    'Price is incorrect',
                    code="price exception",
                    # params={"prices":(),"current_price":price}
                    params={"prices":self.prices,"current_price":price}
                )

class RubricValidation:
    def __init__(self):
        self.rubric_titles:tuple = (
            'trash',"something bad"
        )


    def __call__(self, title: str):
        for title_ in self.rubric_titles:
            if title_ in title:
                raise ValidationError(
                    'Rubric title cant be incorrect',
                    code="rubric exception",
                    params={"titles":self.rubric_titles,"current_title":title_}
                )


class MailExistsValidation:

    def __init__(self):
        self.mails:tuple = (
            '@gmail.com','@mail.ru','@yandex.ru'
        )

    def __call__(self, context: str):
        for mail in self.mails:
            if mail in context:
                raise ValidationError(
                    'Description of announcement cant contain e-mail',
                    code="mail exception",
                    params={"mails":self.mails,"current_mail":mail}
                )




# Модель рубрика
class Rubric(models.Model):

    def title_validation(title: str):
        return RubricValidation()(title=title)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid1, 
                          editable=False)
    name = models.CharField(
        unique=True, help_text='Наименование рубрики', max_length=20, db_index=True, verbose_name='Название',validators=[title_validation]
    )
    is_active = models.BooleanField(default=True, verbose_name='Активна ли рубрика?', blank=True)
    priority = models.DecimalField(default=0, verbose_name='Приоритет', max_digits=20, decimal_places=3)
    created_date = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    changed = models.DateTimeField(verbose_name='Изменено', auto_now=True,null=True)
    parent_rubric = models.ForeignKey('self',on_delete = models.PROTECT,blank=True, null=True, default=None) 


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['priority']
        
# Модель объявление
class Bb(models.Model):


    BANNED_WORDS:tuple = (
        'Товар','товар',
    )
    def kind_validation(kind:str):
            return KindValidation()(kind=kind)
    
    def price_validation(price: int):
        return PriceValidation()(price=price)

    def mail_validation(stroke: str):
        return MailExistsValidation()(context=stroke)
        

    def get_first_rubric():
        return Rubric.objects.first()
    

    def check_title(self):
        for word in Bb.BANNED_WORDS:
            if word in self.title.lower():
                self.title = self.title.replace(word,'*'*len(word))


    

    @property
    def is_more_avg_price(self):
        bbs = list(Bb.objects.all())
        prices = [bb.price for bb in bbs]
        avg_price = sum(prices)/len(prices)
        return "background-color:red" if self.price>avg_price else None






    @property
    def title_and_price(self):
        if self.price:
            return f'{self.title}: {self.price}'
        return self.title


    def save(self,*args,**kwargs):
        print(args,kwargs)
        super().save(*args,**kwargs)


    def delete(self,*args,**kwargs):
        if not self.rubric.is_active:
            super().delete(*args,**kwargs)
        else:
            print(f'cant delete,while rubric {self.rubric} is active!')

    rubric = models.ForeignKey(
        Rubric, null=True, on_delete=models.SET(get_first_rubric), verbose_name='Рубрика')
    
    title = models.CharField(max_length=50, verbose_name='Товар', 
                             unique_for_date='published')
    changed = models.DateTimeField(verbose_name='Изменено', auto_now=True,null=True)
    
    content = models.TextField(null=True, blank=True, verbose_name='Описание',validators=[mail_validation])
    price = models.FloatField(null=True, blank=True, verbose_name='Цена',validators=[price_validation])

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
    kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.__empty__, blank=True,validators=[kind_validation])

    published = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Опубликовано'
    )

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields =  ['-published','title'],
                         name='bb_main',
                         condition=models.Q(price__lte=10000)
                         ),
            models.Index(fields =  ['price','title','rubric'])

            
        ]
        # Общее название того, что мы видим
        verbose_name_plural = 'Объявления'
        # Название конкретной записи
        verbose_name = 'Объявление'
        # как мы сортируем при просмотре в админке
        ordering = ['rubric']
        unique_together = ('title','published')










