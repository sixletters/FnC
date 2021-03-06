from django.shortcuts import render

# Create your views here.


from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class SignUpView(CreateView):
    template_name = 'users/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('photo:list')


    ##validation will be called regardless, hence we overrite this method to include our own validations
    def form_valid(self, form):

        ## our own validations
        to_return = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )

        login(self.request, user)

        ## returns the success_url
        return to_return



class CustomLoginView(LoginView):
    template_name = 'users/login.html'