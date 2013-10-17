from tastypie.cache import NoCache
from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization


class CommonResourceMeta:
        # Disable caching of objects returned from GET
        cache = NoCache()
        list_allowed_methods = []
        detail_allowed_methods = []
        always_return_data = True
        authentication = Authentication()
        authorization = ReadOnlyAuthorization()
