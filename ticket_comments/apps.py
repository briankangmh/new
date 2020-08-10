from django.apps import AppConfig


class TicketCommentsConfig(AppConfig):
    name = 'ticket_comments'
    verbose_name = 'Comment'
    verbose_name_plural = verbose_name

__all__= ['TicketCommentsConfig']
