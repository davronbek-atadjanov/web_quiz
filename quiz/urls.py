from django.urls import path
from .views import question_list, submit_answers, result_view, subject_list

urlpatterns = [
    path('', subject_list, name='subject_list'),
    path('questions/', question_list, name='question-list'),
    path('submit-answers/', submit_answers, name='submit-answers'),
    path('result/', result_view, name='result-view'),
    path('questions/<slug:slug>/', question_list, name='question-list-by-subject'),

]

