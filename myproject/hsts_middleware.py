from django.utils.deprecation import MiddlewareMixin

class HSTSMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response
