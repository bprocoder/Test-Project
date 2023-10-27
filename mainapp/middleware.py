import time
from django.http import HttpResponseForbidden
from django.http import HttpResponsePermanentRedirect
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import render

class RequestLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        now = time.time()

        if ip in self.requests and now - self.requests[ip] < 60:
            return HttpResponseForbidden('Too many requests from this IP')

        self.requests[ip] = now
        response = self.get_response(request)
        return response
    


class RequestThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.cache = cache

    def __call__(self, request):
        # Get the user's IP address
        ip_address = self.get_client_ip(request)

        # Get the current time in minutes
        current_time = int(time.time() / 60)

        # Append the current minute to the cache key to throttle per minute
        cache_key = f'throttle-{ip_address}-{current_time}'

        # Check if the cache key exists and increment the count if it does
        count = self.cache.get(cache_key, 0)
        count += 1

        # If the count exceeds the limit, return a 403 Forbidden response
        if count > settings.REQUEST_THROTTLE_LIMIT:
            return HttpResponseForbidden(render(request, '403.html'))

        # Set the cache key and count for the current minute
        self.cache.set(cache_key, count, settings.REQUEST_THROTTLE_DURATION)

        response = self.get_response(request)

        return response

    def get_client_ip(self, request):
        # Get the IP address from the X-Forwarded-For header if it exists,
        # otherwise use the remote address from the request object
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_list = x_forwarded_for.split(',')
            return ip_list[0].strip()
        return request.META.get('REMOTE_ADDR')
    
    

class RedirectToWWWMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host == 'influencerhiring.com':
            new_host = 'www.influencerhiring.com'
            url = request.build_absolute_uri()
            url = url.replace(host, new_host)
            return HttpResponsePermanentRedirect(url)
        return self.get_response(request)
