from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AddRecord
from .models import Record
# Create your views here.


def home(request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in!')
            return redirect('home')
        else:
            messages.success(request, 'Username or password is incorrect.')
            return render(request, 'home.html')
    else:
        context = {'records': records}
        return render(request, 'home.html', context)


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'You have successfully registered!')
            return redirect('home')
    else:
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    context = {'form': form}
    return render(request, 'register.html', context)


def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)

        context = {'customer_record': customer_record}
        return render(request, 'record.html', context)

    else:
        messages.success(request, 'You must be logged in to access!')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delet_it = Record.objects.get(id=pk)
        delet_it.delete()
        messages.success(request, 'Record has been successfully deleted!')
        return redirect('home')

    else:
        messages.info(request, 'Please loggin to delet this record')
        return redirect('home')


def add_record(request):
    form = AddRecord(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added")
                return redirect('home')

        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You need to logging first!")
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecord(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been updated!')
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})

    else:
        messages.success(request, "You need to logging first!")
        return redirect('home')
