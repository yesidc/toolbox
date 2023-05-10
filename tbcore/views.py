from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

def start_page (request):

    context ={

    }


    return render(request, 'tbcore/start_page.html', context= context)


class ToolBoxLogingView(LoginView):

    def get_success_url(self):
        return reverse_lazy('start-page')