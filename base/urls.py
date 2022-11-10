from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns=[
    path('admin/',admin.site.urls),
    path('Studentmodule/',views.studentmodule, name="studentmodule"),
    path('register/',views.register,name="register"),
    path('login/',views.login,name="login"),
    path('linkorg',views.linkorg,name='linkorg' ),
    path('linkinprofile',views.linkinprofile,name='linkinprofile'),
    path('organization',views.organization,name='organization'),
    path('studentreg',views.studentreg,name='studentreg'),
    path('index',views.index,name='index'),
    path('logout',views.logout,name='logout'),
    path('settings',views.settings,name='settings'),
    path('upload',views.upload,name='upload'),
    path('like-post',views.like_post,name='like-post'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('follow', views.follow, name='follow')


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
