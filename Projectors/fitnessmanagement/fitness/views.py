from django.shortcuts import render, redirect
from django.views import View

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class LoginFormView(View):
    def get(self, request):
        return render(request, 'login_form.html')

    def post(self, request):
        return redirect('index') 
    
class RegisterFormView(View):
    def get(self, request):
        return render(request, 'register_form.html')

    def post(self, request):
        return redirect('login')  