from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from ticket_comments.admin import CommentInline

from .models import UserProfileInfo, Subject, Ticket

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class UserProfileInfoInline(admin.StackedInline):
    model = UserProfileInfo
    can_delete = False
    verbose_name_plural = 'UserProfileInfo'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInfoInline,)


class TicketAdmin(admin.ModelAdmin):
    model = Ticket
    inlines = [CommentInline, ]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Subject)
admin.site.register(Ticket, TicketAdmin)
