from django.shortcuts import render
from .models import OnlineIdea
# Create your views here.


def start_page (request):

    context ={
        'description': OnlineIdea.objects.filter(idea_name='Short Student Introduction/ 2 Truths one lie')[0].short_description
    }


    return render(request, 'tbcore/start_page.html', context= context)