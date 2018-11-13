from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Hobby, Member, Profile
from django.contrib.sessions.models import Session

admin.site.register(Hobby)
admin.site.register(Member)
admin.site.register(Profile)


class SessionAdmin(ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(Session, SessionAdmin)
