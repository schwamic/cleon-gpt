from django.contrib import admin

from conversations.models import AIModel


""" Admin Interface

The django admin should only able to create configuration related records.
Therefore currently only AIModles are registered here.
"""

admin.site.register(AIModel)
