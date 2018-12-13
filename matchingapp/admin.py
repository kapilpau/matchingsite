from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Hobby, Member, Profile, Conversation, Message
from django.contrib.sessions.models import Session

# Binds the user models to the admin page
admin.site.register(Hobby)
admin.site.register(Member)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Conversation)


class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)
