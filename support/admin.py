from django.contrib import admin
from .models import Ticket, ConversationMessage


admin.site.register(Ticket)
admin.site.register(ConversationMessage)