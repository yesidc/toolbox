from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.
# todo delete pdb, it is only for debugging
import pdb

def start_page (request):

    context ={
        'username': request.user.username
    }
    print(f'this is the username: {context["username"]}')
    #pdb.set_trace()

    return render(request, 'tbcore/start_page.html', context= context)