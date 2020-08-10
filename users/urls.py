from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('profile', views.profile, name='profile'),
    path('switch_user_type/<int:ugroup>',
         views.switch_user_type, name='switch_user_type'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('createticket', views.ticket, name='ticket'),
    path('ticket_list', views.ticket_list, name='ticket_list'),
    path('viewticket/<int:id>', views.viewticket, name="viewticket"),
    path('ticket/<int:id>/comment', views.new_comment, name="new_comment"),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name="user/password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name="user/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="user/password_reset_form.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name="user/password_reset_done.html"), name="password_reset_complete"),

]
