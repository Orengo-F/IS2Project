from multiprocessing import context
from operator import length_hint
from tkinter.tix import Form
from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Profile,Post,LikePost


# Create your views here.

studentmodules={}



def studentmodule(request):
    return render(request,'base/studentmodule.html')


def login(request):
    return render(request,'base/login.html')

@login_required(login_url='register')
def linkorg(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)  

    posts = Post.objects.all() 
    return render(request,'base/linkorg.html',{'user_profile': user_profile, 'posts':posts})
@login_required(login_url='register')
def linkinprofile(request):  
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)  
    return render(request,'base/linkinprofile.html',{'user_profile': user_profile})

def organization(request):
    return render(request,'base/organization.html')


def studentreg(request):
    if request.method== "POST":
        #username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        myuser=User.objects.create_user(username, email, password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        messages.success(request, "Your account has been successfully created.")
        return redirect('register')
    return render(request,'base/studentreg.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('studentmodule')
        else:
            messages.info(request, 'Invalid Credentials ')
            return redirect('register')
            

    else:
        return render(request, 'base/register.html')

@login_required(login_url='register')
def index(request):
    return render(request,'base/index.html')

def logout(request):
    auth.logout(request)
    return redirect('login')




@login_required(login_url='register')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            about = request.POST['about']
            email = request.POST['email']
            lang = request.POST['lang']
            experience = request.POST['experience']
            education = request.POST['education']
            skills = request.POST['skills']
            internship = request.POST['internship']

            user_profile.profileimg =image
            user_profile.about=about
            user_profile.email=email
            user_profile.lang=lang
            user_profile.experience=experience
            user_profile.education=education
            user_profile.skills=skills
            user_profile.internship=internship
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            about = request.POST['about']
            email = request.POST['email']
            lang = request.POST['lang']
            experience = request.POST['experience']
            education = request.POST['education']
            skills = request.POST['skills']
            internship = request.POST['internship']

            user_profile.profileimg =image
            user_profile.about=about
            user_profile.email=email
            user_profile.lang=lang
            user_profile.experience=experience
            user_profile.education=education
            user_profile.skills=skills
            user_profile.internship=internship
            user_profile.save()

        return redirect('settings')


    
    return render(request,'base/setting.html',{'user_profile':user_profile})


@login_required(login_url='register')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        image= request.FILES.get('image_upload')
        caption= request.POST['caption']

        new_post= Post.objects.create(user=user, image=image,caption=caption)
        new_post.save()

        return redirect('linkorg')
    else:
        return redirect('linkorg')
    return HttpResponse('<h1> Upload View </h1>')

def like_post(request):
    
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter == None:
        new_like =LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('linkorg')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('linkorg')

@login_required(login_url='register')
def profile (request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    context={
        'user_object':user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length':user_post_length,

    }

    return render(request,'base/linkinprofile.html',context)


