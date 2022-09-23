from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.


def start_page (request):

    context ={

    }


    return render(request, 'tbcore/start_page.html', context= context)