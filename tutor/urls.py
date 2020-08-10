from django.urls import path , include ,re_path

from . import views


urlpatterns = [
    path('', views.index, name='tutor'),
    path('profile', views.profile, name='tutor_profile'),
    path('question/<int:qid>', views.view_question, name='tutor_question'),
    path('accept_question/<int:qid>', views.accept_question, name='accept_question'),
    path('add_answer/<int:qid>', views.add_answer, name='tutor_answer'),
    path('answer/<int:qid>', views.view_answer, name='view_tutor_answer'),
    path('history', views.tutor_history, name='tutor_history'),
    path('status/<int:val>', views.status, name='tutor_status'),
    path('answer/<int:aid>/update', views.update_answer , name='update_answer'),
    path('deleteanswer/<int:aid>', views.delete_answer, name='delete_answer'),
]