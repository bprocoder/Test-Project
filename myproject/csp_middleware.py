from django.utils.deprecation import MiddlewareMixin

class CSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        csp_value = "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.google.com/recaptcha/api.js https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit; style-src 'self' 'unsafe-inline';"
        response["Content-Security-Policy"] = csp_value
        return response
