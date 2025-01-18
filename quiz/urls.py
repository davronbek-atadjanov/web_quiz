# urls.py
from django.urls import path
from .views import question_list, submit_answers, result_view

urlpatterns = [
    path('questions/', question_list, name='question-list'),
    path('submit-answers/', submit_answers, name='submit-answers'),
    path('result/', result_view, name='result-view'),
]
