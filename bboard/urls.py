from django.urls import path
from .views import index, by_rubric, search, BbCreateView, RubricCreateView

urls = [
    path('bboard/', by_rubric, name='index'),
    path('bboard/<str:rubric_id>/', by_rubric, name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('addRubric/', RubricCreateView.as_view(), name='addRubric'),
    path("search/", search, name="search"),
]
