from django.contrib.auth.forms import (
    UserCreationForm as AuthUserCreationForm,
    UserChangeForm as AuthUserChangeForm)

from .models import User


class UserCreationForm(AuthUserCreationForm):
    '''
    A form that creates a user, with no privileges, from the given email and
    password.
    '''

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(AuthUserChangeForm):
    '''A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    '''

    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = User
