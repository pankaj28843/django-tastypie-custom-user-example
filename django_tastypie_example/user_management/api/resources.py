from tastypie.authentication import (BasicAuthentication, MultiAuthentication,
                                     ApiKeyAuthentication)
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from tastypie_extras.exceptions import CustomBadRequest
from tastypie_extras.resources import CommonResourceMeta
from ..models import User
from ..utils import validate_password
from .authorization import CustomAuthorization


class UserResource(ModelResource):
    '''Get and update user profile.'''

    class Meta(CommonResourceMeta):
        # For authentication, allow both basic and api key so that the key
        # can be grabbed, if needed.
        authentication = MultiAuthentication(BasicAuthentication(),
                                             ApiKeyAuthentication())
        authorization = CustomAuthorization()

        list_allowed_methods = ['get']
        detail_allowed_methods = ['get', 'patch', 'put']

        queryset = User.objects.all().select_related('api_key')
        fields = ['email', 'first_name', 'last_name']
        resource_name = 'user'

    def hydrate(self, bundle):
        raw_password = bundle.data.pop('password')
        if not validate_password(raw_password):
            raise CustomBadRequest(
                code='invalid_password',
                message='Your password is invalid.')

        bundle.obj.set_password(raw_password)

        return bundle

    def dehydrate(self, bundle):
        if bundle.obj.pk == bundle.request.user.pk:
            bundle.data['key'] = bundle.obj.api_key.key

        return bundle

    def authorized_read_list(self, object_list, bundle):
        # Return the profile of user making api reqeust.
        return object_list.filter(id=bundle.request.user.id).select_related()


class CreateUserResource(ModelResource):
    '''Endpoint to create a new account for a user.'''

    class Meta(CommonResourceMeta):
        queryset = User.objects.all()

        list_allowed_methods = ['post']
        detail_allowed_methods = []

        authorization = Authorization()
        resource_name = 'create_user'
        fields = ['email', 'first_name', 'last_name']

    def obj_create(self, bundle, **kwargs):
        REQUIRED_FIELDS = ('email', 'first_name', 'last_name',
                           'password')
        for field in REQUIRED_FIELDS:
            if field not in bundle.data:
                raise CustomBadRequest(
                    code='missing_key',
                    message=('Must provide {missing_key} when creating a'
                             ' user.').format(missing_key=field))

        email = bundle.data['email']
        try:
            if User.objects.filter(email=email):
                raise CustomBadRequest(
                    code='duplicate_exception',
                    message='That email is already associated with some user.')
        except User.DoesNotExist:
            pass

        raw_password = bundle.data.pop('password')
        if not validate_password(raw_password):
            raise CustomBadRequest(
                code='invalid_password',
                message='Your password is invalid.')

        bundle.obj.set_password(raw_password)

        return super(CreateUserResource, self).obj_create(bundle, **kwargs)
