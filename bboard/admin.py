from django.contrib import admin
from .models import Bb, Rubric

# Register your models here.
# Регистрируем нашу модель в админке для работы
# с ней же 
class BbAdmin(admin.ModelAdmin):
    # Общее отображение
    list_display = ('title', 'content', 'price', 'published', 'rubric','changed')
    # По каким ссылкам мы можем провалиться в запись
    list_display_links = ('title', 'content')
    list_filter = ( 'rubric',)

    # По каким полям можно искать записи
    search_fields = ('title', 'content', 'price','kind')
    search_help_text = 'По названию, контенту и цене'


# Регистрируем модель рубрики для админки
class RubricAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','created_date','changed')
    list_display_links = ('name','created_date',)
    search_fields = ('name',)
    search_help_text = 'Поиск по наименованию рубрики'


admin.site.register(Rubric, RubricAdmin)
admin.site.register(Bb, BbAdmin)