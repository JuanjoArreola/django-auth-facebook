from dataclasses import dataclass

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class FacebookUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    facebook_id = models.CharField(max_length=32, unique=True, verbose_name=_('Facebook Id'))
    token = models.TextField('Token')
    created = models.DateTimeField(_('Created'), auto_now_add=True)


@dataclass
class TokenMetadata:
    auth_type: str
    sso: str


@dataclass
class DebugToken:
    app_id: str
    user_id: str
    type: str
    application: str
    data_access_expires_at: int
    expires_at: int
    is_valid: bool
    scopes: list
    metadata: TokenMetadata = None


@dataclass
class Picture:
    url: str


@dataclass
class Profile:
    id: str
    name: str
    email: str
    first_name: str
    last_name: str
    picture: Picture


@dataclass
class FacebookError:
    message: str
    type: str
    code: str
    fbtrace_id: str
