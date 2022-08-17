from django.shortcuts import render
from .models import OnlineIdea
# Create your views here.


def start_page (request):

    context ={
        'description': OnlineIdea.objects.filter(idea_name='Instructor introduction video')[0]
    }


    return render(request, 'tbcore/start_page.html', context= context)