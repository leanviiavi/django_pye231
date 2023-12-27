from django.urls import path
from .views import index, by_rubric, BbCreateView, RubricCreateView

urlpatterns = [
    path('bboard/', by_rubric, name='index'),
    path('bboard/<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('addRubric/', RubricCreateView.as_view(), name='addRubric')
]
