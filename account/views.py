from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from .forms import UserLoginForm
from django.contrib.auth import logout
from django.contrib import messages


class LoginUser(LoginView):
    form_class = UserLoginForm
    template_name = 'login.html'

    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


def logout_view(request):
    logout(request)
    return redirect('/')
