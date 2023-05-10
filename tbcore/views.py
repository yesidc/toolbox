from urllib.parse import urlencode

import requests
from django.shortcuts import render,  reverse
from django.contrib.auth.models import User
# Create your views here.
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


def start_page(request):
    context = {

    }

    return render(request, 'tbcore/start_page.html', context=context)


class ToolBoxLogingView(LoginView):

    def get_success_url(self):
        # check if category_name and idea_id are in the url

        if 'category_name' in self.request.GET and 'idea_id' in self.request.GET:
            # get the category_name and idea_id from the url
            category_name = self.request.GET['category_name']
            idea_id = self.request.GET['idea_id']
            # get the url for the idea_overview_detail view
            url = f"{reverse('idea_overview_detail', kwargs={'category_name': category_name, 'idea_id': idea_id})}?{urlencode({'preserve_note': 'True'})}"
            return url

        return reverse_lazy('start-page')
