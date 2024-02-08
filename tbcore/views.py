from urllib.parse import urlencode
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,  reverse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, UserModel
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from plan.helpers import has_plan
from .models import Plan
from .tokens import account_activation_token
from .forms import SignUpForm
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator



def start_page(request):
    context = { }
    return render(request, 'tbcore/start_page.html', context=context)


class ToolBoxResetPasswordView(PasswordResetView,PasswordResetForm):
    template_name = 'password_reset/password_reset.html'
    success_url = reverse_lazy('password_reset_done')

    def send_email(self,
                email,
                use_https=False,
                token_generator=default_token_generator,
                extra_email_context=None,):
            """
            Generate a one-use only link for resetting password and send it to the
            user.
            """
            current_site = get_current_site(self.request)
            site_name = current_site.name
            domain = current_site.domain

            email_field_name = UserModel.get_email_field_name()
            for user in self.get_users(email):
                user_email = getattr(user, email_field_name)
                context = {
                    "email": user_email,
                    "domain": domain,
                    "site_name": site_name,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": token_generator.make_token(user),
                    "protocol": "https" if use_https else "http",
                    **(extra_email_context or {}),
                }
                subject = 'Reset your password'
                html_message = render_to_string('password_reset/password_reset_email.html', context)

                from_email = settings.DEFAULT_FROM_EMAIL
                to_email = user_email

                # Send the email
                email = EmailMultiAlternatives(subject, html_message, from_email, [to_email])
                email.attach_alternative(html_message, "text/html")
                email.send()


    def form_valid(self, form):

        self.send_email(email=form.cleaned_data["email"])
        return HttpResponseRedirect(self.get_success_url())



class SignUpView(CreateView):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    form_class = SignUpForm

    def form_valid(self, form):
        # crate user but do not save it yet
        user = form.save(commit=False)
        user.is_active = False

        # save user object
        user.save()

        # Send the activation email to the user
        self.send_activation_email(user)

        # Return the response
        return super().form_valid(form)

    def send_activation_email(self, user):
        # Generate the token for activation
        token = account_activation_token.make_token(user)

        # Build the activation URL
        # encode the user's primary key
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(self.request).domain
        activation_url = reverse('activate', kwargs={'uidb64': uid, 'token': token})
        activation_link = f'http://{domain}{activation_url}'

        # Compose the email
        subject = 'Activate Your Account'
        html_message = render_to_string('registration/activation_email.html', {
            'user': user,
            'activation_link': activation_link,
        })
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        # Send the email
        email = EmailMultiAlternatives(subject, html_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()


class ActivateAccountView(View):

    def send_signup_email(self, user):
        subject = 'Welcome to The Toolbox!'
        html_message = render_to_string('registration/signup_welcome_email.html', {'user': user})
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = user.email

        email = EmailMultiAlternatives(subject, plain_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.send()

    def get(self, request, uidb64, token):
        User = get_user_model()
        # decode the user's primary key from the url and get the user
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            # no user was found given the decoded id
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            self.send_signup_email(user)
            return redirect('start-page')
        else:
            # Handle invalid activation link
            # todo delete user if activation link is invalid or resend activation email
            return HttpResponse('Activation link is invalid!')



# def activate_account(request, uidb64, token):
#     User = get_user_model()
#     # decode the user's primary key from the url and get the user
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         # no user was found given the decoded id
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#
#         return redirect('start-page')
#     else:
#         # Handle invalid activation link
#         # todo delete user if activation link is invalid
#         return HttpResponse('Activation link is invalid!')
#



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
            messages.success(self.request, f'Welcome back! We loaded your course plan '
                                           f'"{plan.plan_name}" for you to pick up where you left off.')
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
