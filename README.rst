=====
Django Auth Facebook
=====

Auth Facebook is a Django app to Sign up / Log in using Facebook

Quick start
-----------

1. Add "facebook_auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'facebook_auth.apps.FacebookAuthConfig',
    ]

2. Set the facebook app id and secret variables::

    FACEBOOK_ID = variables['FACEBOOK_ID']
    FACEBOOK_SECRET = variables['FACEBOOK_SECRET']

3. Create a subclass of ``FacebookAuth`` overriding the method ``get_user``::

    class ProjectFacebookAuth(FacebookAuth):

        def get_user(self, profile: Profile):
            User.objects.create_user(username, profile.email, first_name=profile.first_name,
                                     last_name=profile.last_name)

In this method you get or create an instance of ``django.contrib.auth.models.User`` and make any additional configuration
needed by your project.

4. Run ``python manage.py migrate`` to create the facebook-auth models.

