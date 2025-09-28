from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm
from .utils import compress_image

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user.set_password(form.cleaned_data['password1'])
                if 'image' in request.FILES:
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(300,300))
                    user.image_small.save(image_name, optimized_image, save=False)
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(800,800))
                    user.image_medium.save(image_name, optimized_image, save=False)
                    optimized_image, image_name = compress_image(request.FILES['image'], size=(1200,1200))
                    user.image_large.save(image_name, optimized_image, save=False)
                user.save()

                auth_login(request, user)
                return redirect('categories:show_categories')
            except Exception as e:
                messages.error(request, f'Помилка при реєстрації: {str(e)}')
        else:
            messages.success(request, 'Виправте помилки в формі')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
 
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                auth_login(request, user)
                return redirect('categories:show_categories')
        else:
            messages.error(request, 'Виправте помилки в формі')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('homepage')