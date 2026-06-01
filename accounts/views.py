from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if form.cleaned_data.get('credit_opt_in'):
                from finance.models import CustomerProfile
                CustomerProfile.objects.get_or_create(user=user)
            return redirect('login')
        
    else:
        form = UserRegistrationForm()
    return render(request,'registration/registration.html', {'form':form})

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')  # Redirect staff to their dashboard
    context = {
        'user': request.user,
    } 
    return render(request, 'includes/dashboard.html', context)