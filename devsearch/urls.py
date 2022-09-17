from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from rest_framework.authtoken import views


urlpatterns = [
    path('admin/', admin.site.urls),
    # INCLUDES ALL URLS THAT ARE COMING FROM THE APP FOLDER NAMED 'projects'
    path('projects/', include('projects.urls'),),
    path('', include('users.urls'),),
    path('api/', include('api.urls'),),

    # redirects user to email input page
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'), name='reset_password'),
    # send user an email link
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name='password_reset_done'),
    # 
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset.html'), name='password_reset_confirm'),
    # 
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name='password_reset_complete'),
]


# TELLS DJANGO THE URL TO LOOK FOR MEDIA FILES
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# TELLS DJANGO THE URL TO LOOK FOR STATIC FILES IN PRODUCTION MODE
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)