from oauth2_provider.views.generic import ProtectedResourceView

class ApiEndPoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Protected with OAuth2')
