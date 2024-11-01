from django.contrib import admin

from conversations.models import AIModel, AIFunction

admin.site.register(AIModel)
admin.site.register(AIFunction)
