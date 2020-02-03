from django.conf import settings
from django.contrib.auth.models import User


class EmailOrUsernameModelBackend(object):
    '''
    This is the ModelBackend that allows authentication with either
    a username or an email address. 
    '''
    
    def authenticate(username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    
    def get_user(username):
        try:
            return User.objects.get(pk=username)
        except User.DoesNotExist:
            return None