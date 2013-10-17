from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        '''
        Creates and saves a User with the given email and password.
        '''
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser, PermissionsMixin):
    '''
    Inherits from both the AbstractBaseUser and PermissionMixin.
    '''
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def date_joined(self):
        return self.created

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.get_full_name()


#===========================================================================
# SIGNALS
#===========================================================================
def signals_import():
    ''' A note on signals.

    The signals need to be imported early on so that they get registered
    by the application. Putting the signals here makes sure of this since
    the models package gets imported on the application startup.
    '''
    # Defining create_api_key manually here to avoid
    # https://github.com/toastdriven/django-tastypie/issues/1009
    def create_api_key(sender, **kwargs):
        """
        A signal for hooking up automatic ``ApiKey`` creation.
        """
        # By the time next line is executed, AUTH_USER_MODEL will be already
        # configured.
        from tastypie.models import ApiKey
        if kwargs.get('created') is True:
            ApiKey.objects.create(user=kwargs.get('instance'))

    models.signals.post_save.connect(create_api_key, sender=User)

signals_import()
