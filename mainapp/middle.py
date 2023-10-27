from mainapp.models import Alluserlogs

class URLHitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        url = request.path
        method = request.method
        user = request.user

        # Pass the request to the next middleware or view
        response = self.get_response(request)

        # Get the status code from the response
        status_code = response.status_code
        
        if status_code >= 200 and status_code < 300:
            status_type = "Success"
        elif status_code >= 300 and status_code < 400:
            status_type = "Redirection"
        elif status_code >= 400 and status_code < 500:
            status_type = "Client Error"
        elif status_code >= 500 and status_code < 600:
            status_type = "Server Error"
        else:
            status_type = "Unknown"

        # Save the URL hit to the database
        Alluserlogs.objects.create(path=url, method=method, userid=str(user), statuscode=status_code,statustype=status_type)

        return response
