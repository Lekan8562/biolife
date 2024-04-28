from django.shortcuts import render,redirect
from .forms import UserForm

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect(new_user)
        else:
            form = UserForm()
        return render(request,'registration/login.html',{'form':form})
