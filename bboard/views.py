from typing import Any
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from .models import Bb, Rubric
from django.views.generic.edit import CreateView
from .forms import BbForm, RubricForm
from django.urls import reverse_lazy

""" Контроллер для формы Bb """
class BbCreateView(CreateView):
    """ какая страница будет рендериться """
    template_name = 'create.html'
    """ к какой модели формы мы цепляемся """
    form_class = BbForm
    """ при успешной отправки и успешном выполнении
     действий с формой попадаем в endpoint 
      /bboard/ """
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context

class RubricCreateView(CreateView):
    template_name = 'create.html'
    form_class = RubricForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        return context
    


def index(request):
    """ формирую ответ в виде страницы """
    template = loader.get_template('index.html')
    """ получаем список всех записей """
    bbs = Bb.objects.order_by('-published')
    context = {'bbs' : bbs}
    """ отправляем клиенту ответ от сервера в виде страницы """ 
    return HttpResponse(template.render(context, request))


def by_rubric(request, rubric_id=None):
    """ Если рубрика есть, то учитывая ее получаем список
       объявлений и текущую рубрику. Если нет, то текущая рубрика
       по умолчанию будет None, а в список объявлений попадут они все
    """

    if rubric_id:
        """ выдаем объявления по рубрике """
        bbs = Bb.objects.filter(rubric=rubric_id)
        """ определяем какая рубрика сейчас активна """
        current_rubric = Rubric.objects.get(pk=rubric_id)
    else:
        """ получаем список всех объявлений """
        bbs = Bb.objects.all()
        """ текущая рубрика пуста """
        current_rubric = None
    """ выдаем все рубрики """
    rubrics = Rubric.objects.all()
    
    """ определяем данные (контекст) который будет выводиться
       на саму страницу """
    context = {
        'bbs' : bbs,
        'rubrics' : rubrics,
        'current_rubric' : current_rubric, 
        'title' : 'Рубрики',
    }
    """ вернем страницу с ответом клиенту """
    return render(request, 'by_rubric.html', context)