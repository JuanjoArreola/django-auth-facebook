from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FacebookAuthConfig(AppConfig):
    name = 'facebook_auth'

    verbose_name = _('Facebook Auth')
