from django.urls import path, include, re_path

from . import views


urlpatterns = [
    path('', views.index, name='tutee'),
    path('profile', views.profile, name='tutee_profile'),
    path('question', views.question, name='tutee_question'),
    path('question/<int:qid>', views.view_question, name='tutee_question'),
    path('question/search', views.search_question, name='search_question'),
    path('deletequestion/<int:qid>', views.delete_question, name='delete_question'),
    path('answer/<int:qid>', views.view_answer, name='tutee_answer'),
    path('answer/<int:aid>/feedback', views.tutor_feedback, name='tutor_feedback'),
    path('history', views.tutee_question_history, name='tutee_question_history'),
    path('viewtutor/<int:id>', views.view_tutor, name='view_tutor'),
    path('findtutor', views.find_tutor, name='find_tutor'),
]
