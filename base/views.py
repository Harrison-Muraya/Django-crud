from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from . models import Users, Post
from . forms import PostForm, CreateUserForm
# from .forms import UserForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password') 

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have logged In Welcome back')
                return redirect('post_list')
            else:
                messages.info(request, 'Username OR password is incorrect')

        return render(request, 'base/login.html')

# User logout view

def logoutUser(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('post_list')


# User registration
def register(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            # validate password
            if password != confirm_password:
                messages.error(request, 'password do not match')
                return redirect('register')
            
            # Check if user with the same email already exists
            # if User.objects.filter(email=email).exists():
            #     messages.error(request, 'Email already in use')
            #     return redirect('register')
            
            # create user
            user = User.objects.create_user(
                username= username,
                email=email,
                first_name=firstname,
                last_name=lastname,
                password=password
            )

            # Log the user in automatically after registration
            messages.success(request, 'Registration successful!')
            return redirect('loginPage')  # Redirect to your post list or homepage after registration


        return render(request, 'base/register.html')
# create post
@login_required(login_url='loginPage')
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
@login_required(login_url='loginPage')
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'base/post_details.html', {'post': post})

def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'base/post_list.html', {'posts': posts})

# Update post
@login_required(login_url='loginPage')
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
@login_required(login_url='loginPage')
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'base/post_confirm_delete.html', {'post': post})