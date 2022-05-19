from django.contrib import admin
from django.contrib.admin import register

from facebook_auth.models import FacebookUser


@register(FacebookUser)
class FacebookUserAdmin(admin.ModelAdmin):
    list_display = ['facebook_id', 'user', 'created']
