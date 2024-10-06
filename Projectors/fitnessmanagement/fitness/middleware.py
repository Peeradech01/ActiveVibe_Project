from django.http import Http404
from django.shortcuts import render

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            return render(request, 'exceptions/404.html', status=404)
        elif response.status_code == 403:
            return render(request, 'exceptions/403.html', status=403)
        return response