from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from users.forms import UserRegisterationForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    else:
        form = UserRegisterationForm()
    return render(request, "registration/sign_up.html", {'form':form})

def dashboard(request):
    return render(request, "users/dashboards.html") 

def login_redirect(request):
    return redirect('home')

def logout_redirect(request):
    return render(request, "registration/logout.html")
    
# def password_reset(request):
#     return render(request, "registration/password_reset_form.html") 