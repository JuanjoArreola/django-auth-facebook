from abc import ABC, abstractmethod

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from core.exceptions import UserInputError
from facebook_auth.models import FacebookUser, DebugToken, Profile
from facebook_auth.serializers import DebugContainerSerializer, FacebookErrorContainerSerializer, ProfileSerializer


class FacebookAuth(ABC):

    def __init__(self):
        self.app_id = settings.FACEBOOK_ID
        self.secret = settings.FACEBOOK_SECRET
        self.permissions = {'public_profile', 'email'}

    def login_or_signup(self, token):
        info = self.validate_login_token(token)
        try:
            facebook_user = FacebookUser.objects.get(facebook_id=info.user_id)
            return self._update_token(token, facebook_user), False
        except FacebookUser.DoesNotExist:
            if not self.permissions.issubset(info.scopes):
                raise UserInputError(_('Some required permission were not granted'), 'facebook_auth.permissions',
                                     _('Allow the required permissions to continue'))
            return self.signup(token), True

    def _update_token(self, token, facebook_user):
        facebook_user.token = token
        facebook_user.save(update_fields=['token'])
        return facebook_user

    def signup(self, token):
        profile = self.get_profile(token)
        user = self.get_user(profile)
        return FacebookUser.objects.create(user=user, facebook_id=profile.id, token=token)

    @abstractmethod
    def get_user(self, profile: Profile):
        pass

    def get_profile(self, token, fields=None) -> Profile:
        fields = fields or ['id', 'name', 'first_name', 'last_name', 'picture', 'email']
        url = f'https://graph.facebook.com/me?fields={",".join(fields)}&access_token={token}'
        response = requests.get(url)
        serializer = ProfileSerializer(data=self._success_json(response))
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def validate_login_token(self, token):
        info = self.debug_token(token)
        if not info.is_valid:
            raise UserInputError(_("It wasn't possible to validate the account"),
                                 'facebook_auth.debug_token')
        return info

    def debug_token(self, token) -> DebugToken:
        url = f'https://graph.facebook.com/debug_token?input_token={token}&access_token={self.app_id}|{self.secret}'
        response = requests.get(url)
        serializer = DebugContainerSerializer(data=self._success_json(response))
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def _success_json(self, response):
        if 200 <= response.status_code < 400:
            return response.json()
        else:
            serializer = FacebookErrorContainerSerializer(data=response.json())
            serializer.is_valid(raise_exception=True)
            error = serializer.save()
            raise UserInputError(error.message, error.code)
