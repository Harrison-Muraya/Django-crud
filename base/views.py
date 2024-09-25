from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Users, Post
from . forms import PostForm, CreateUserForm
# from .forms import UserForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('post_list')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'base/login.html', {'form': form})
# User logout view
@login_required
def logout(request):
    auth_logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


# User registration
def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # validate password
        if password != confirm_password:
            messages.error(request, 'password do not match')
            return redirect('base/register.html')
        
        # create user
        user = User.objects.create_user(
            username= firstname,
            email=email,
            first_name=firstname,
            last_name=lastname,
            password=password
        )

         # Log the user in automatically after registration
        auth_login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('post_list')  # Redirect to your post list or homepage after registration


    return render(request, 'base/register.html')

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'base/post_form.html', {'form': form})


# View a single post
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'base/post_details.html', {'post': post})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'base/post_list.html', {'posts': posts})

# Update post
def update_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'base/post_form.html', {'form': form})

# Delete post
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'base/post_confirm_delete.html', {'post': post})