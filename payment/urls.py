from django.urls import path, include, re_path

from . import views


urlpatterns = [
    path('make_payment', views.make_payment, name='make_payment'),
    path('transaction_history', views.transaction_history,
         name='transaction_history'),
    path('ad_watched', views.ad_watched, name="ad_watched"),
    path('add_money_to_wallet', views.add_money_to_wallet,
         name="add_money_to_wallet"),
    path('active_chat_session/<int:qid>', views.active_chat_session,
         name="active_chat_session")

]
