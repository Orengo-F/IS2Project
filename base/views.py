from ast import Delete
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
from .models import Profile,Post,LikePost, FollowersCount,Orgsettings,Jobs


# Create your views here.

studentmodules={}



def studentmodule(request):
    return render(request,'base/studentmodule.html')



def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password= request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('organization')
        else:
            messages.info(request, 'Invalid Credentials ')
            return redirect('login')
    else:
        return render(request, 'base/login.html')


@login_required(login_url='register')
def linkorg(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)  

    posts = Post.objects.all() 
    return render(request,'base/linkorg.html',{'user_profile': user_profile, 'posts':posts,'user_object':user_object})
@login_required(login_url='register')
def linkinprofile(request):  
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)  



    return render(request,'base/linkinprofile.html',{'user_profile': user_profile,'user_object':user_object})

def orgprof(request):  
    user_object = User.objects.get(username=request.user.username)
    user_profile = Orgsettings.objects.get(user=user_object)  



    return render(request,'base/orgprof.html',{'user_profile': user_profile,'user_object':user_object})


def organization(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)  

    posts = Post.objects.all() 
    return render(request,'base/organization.html',{'user_profile': user_profile, 'posts':posts,'user_object':user_object})
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
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('linkorg')
    else:
        return redirect('linkorg')

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

    follower = request.user.username
    user=pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Remove connection'
    else:
        button_text='Connect'

    user_followers =len(FollowersCount.objects.filter(user=pk))
    user_following = len( FollowersCount.objects.filter(follower=pk))

    



    context={
        'user_object':user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length':user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,

    }

    return render(request,'base/linkinprofile.html',context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('linkinprofile')

def orgjobs(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)  

    jobs = Jobs.objects.all() 
    return render(request,'base/orgjobs.html',{'user_profile': user_profile, 'jobs':jobs,'user_object':user_object})




def chats(request):
    context={}
    return render(request,'base/chat.html',context)

def base(request):
    context={}
    return render(request,'base/base.html',context)

def details(request):
    return render(request,'base/detail.html')

def studentjobs(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)  

    jobs = Jobs.objects.all() 
    return render(request,'base/studentjobs.html',{'user_profile': user_profile, 'jobs':jobs,'user_object':user_object})

def orgsettings(request):
    user_profile=Orgsettings.objects.get(user=request.user)

    if request.method == 'POST':

        if request.FILES.get('image') == None:
            image = user_profile.orgimg
            about = request.POST['about']
            email = request.POST['email']


            user_profile.orgimg =image
            user_profile.about=about
            user_profile.email=email
            user_profile.save()

        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            about = request.POST['about']
            email = request.POST['email']

            user_profile.orgimg =image
            user_profile.about=about
            user_profile.email=email
            user_profile.save()

        return redirect('orgsettings')


    return render(request,'base/orgsettings.html')

def jobs(request):
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Jobs.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('orgjobs')
    else:
        return redirect('orgjobs')

def alumnilogin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password= request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('organization')
        else:
            messages.info(request, 'Invalid Credentials ')
            return redirect('alumnilogin')
    else:
        return render(request,'base/alumnilogin.html')