from django.shortcuts import render

class CustomMiddleware:
    def __init__(self, get_response):
        # Initialize the middleware with a reference to the next middleware in the chain
        self.get_response = get_response

    def __call__(self, request):
        # Call the next middleware in the chain and get the response
        response = self.get_response(request)
        
        # If the response is a 404 error, render a custom 404 template
        if response.status_code == 404:
            return render(request, 'exceptions/404.html', status=404)
        
        # If the response is a 403 error, render a custom 403 template
        elif response.status_code == 403:
            return render(request, 'exceptions/403.html', status=403)
        
        # Otherwise, return the original response
        return response