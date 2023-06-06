from urllib.parse import urlencode
from django.contrib import messages
from django.shortcuts import render,  reverse
# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from plan.helpers import has_plan
from .models import Plan
from .forms import SignUpForm



def start_page(request):
    context = { }


    return render(request, 'tbcore/start_page.html', context=context)


class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm

    def form_valid(self, form):
        # Perform additional actions here
        # For example, send a welcome email to the user

        # Call the parent class's form_valid() method
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context

class ToolBoxLogoutView(LogoutView):
    next_page = reverse_lazy('start-page')
    def dispatch(self, request, *args, **kwargs):
        # Clear local storage

        return super().dispatch(request, *args, **kwargs)


class ToolBoxLogingView(LoginView):



    def get_success_url(self):

        # loads a users plan if they have one
        if has_plan(self.request):
            plan= Plan.objects.get_user_plans(self.request.user).last()
            self.request.session['current_user_plan'] = plan.pk
            self.request.session['current_user_plan_name'] = plan.plan_name
            messages.success(self.request, f'Welcome back {self.request.user.username}! We have automatically loaded '
                                           f'"{plan.plan_name}" course plan for you to continue working on it.')
        else:
            # create a plan for the user and add it to the session
            plan = Plan.objects.create(user=self.request.user,
                                       plan_name='My Plan')
            self.request.session['current_user_plan'] = plan.pk
            self.request.session['current_user_plan_name'] = plan.plan_name
            messages.success(self.request, f'Welcome {self.request.user.username}! We have automatically crated a plan '
                                           f"for you to get started right away!. Click on the plan's name (on the "
                                           f"left)  to change " 
                                           f'its name.')


        # check if category_name and idea_id are in the url
        if 'category_name' in self.request.GET and 'idea_id' in self.request.GET:
            # get the category_name and idea_id from the url
            category_name = self.request.GET['category_name']
            idea_id = self.request.GET['idea_id']
            # get the url for the idea_overview_detail view
            url = f"{reverse('idea_overview_detail', kwargs={'category_name': category_name, 'idea_id': idea_id})}?{urlencode({'preserve_note': 'True'})}"
            return url
        # if user logs in from building block page, redirect to building block page user was on
        if 'category_url' in self.request.GET and 'next_page' in self.request.GET:
            return reverse('show_block', kwargs={'category_url': self.request.GET['category_url'], 'next_page': self.request.GET['next_page']})

        return reverse_lazy('start-page')
