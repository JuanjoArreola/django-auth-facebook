=====
Django Auth Facebook
=====

Auth Facebook is a Django app to Sign up / Log in using Facebook

Quick start
-----------
1. Install::

    pip install https://github.com/JuanjoArreola/django-auth-facebook.git@0.7.4

or added it to your requirements.txt::

    git+https://github.com/JuanjoArreola/django-auth-facebook.git@0.7.4

2. Add "facebook_auth" to your INSTALLED_APPS settings::

    INSTALLED_APPS = [
        ...
        'facebook_auth.apps.FacebookAuthConfig',
    ]

3. Set the facebook app id and secret variables::

    FACEBOOK_ID = variables['FACEBOOK_ID']
    FACEBOOK_SECRET = variables['FACEBOOK_SECRET']

4. Create a subclass of ``FacebookAuth`` overriding the method ``get_user``::

    class CustomFacebookAuth(FacebookAuth):

        def get_user(self, profile: Profile):
            try:
                return Customer.objects.get(user__email=profile.email).user
            except Customer.DoesNotExist:
                user = User.objects.create_user(get_username(profile), profile.email, first_name=profile.first_name,
                                                last_name=profile.last_name)
                Customer.objects.create(user=user)
                return user

In this method you get or create an instance of ``django.contrib.auth.models.User`` and make any additional configuration
needed by your project.

5. Run ``python manage.py migrate`` to create the facebook-auth models.
