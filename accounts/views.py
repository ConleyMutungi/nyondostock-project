from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = UserRegistrationForm()
    return render(request,'registration/registration.html', {'form':form})