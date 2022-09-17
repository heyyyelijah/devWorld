from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views



# 
urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('account/', views.userAccount, name='account'),

    path('', views.profiles, name='profiles'),
    path('user-profile/<str:pk>/', views.userProfiles, name='user-profile'),
    path('edit-account/', views.editAccount, name='edit-account'),

    path('create-skill/', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>/', views.message, name='message'),
    path('send-message/<str:pk>/', views.sendMessage, name='send-message'),
]


# TELLS DJANGO THE URL TO LOOK FOR MEDIA FILES
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# TELLS DJANGO THE URL TO LOOK FOR STATIC FILES IN PRODUCTION MODE
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)