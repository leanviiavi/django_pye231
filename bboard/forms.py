from django.forms import ModelForm
from .models import Bb, Rubric


""" Создаем модель формы для Bb """
class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = (
            'title', 'content', 'price', 'rubric'
        )


""" Создаем модель формы для Bb """
class RubricForm(ModelForm):
    class Meta:
        model = Rubric
        fields = ('name', 'is_active', 'priority')
