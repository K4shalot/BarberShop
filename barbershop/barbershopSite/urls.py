"""
URL configuration for barbershopSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from berberApp.views import get_available_times, main_view, booking, success, barber_dashboard,edit_unavailable_slots,delete_booking
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_view, name='main'),
    path('booking/', booking, name='booking'),
    path('success/', success, name='success'),
    path('booking/get-available-times/', get_available_times, name='get_available_times'),
    path('barber/dashboard/', barber_dashboard, name='barber_dashboard'),
    path('barber/edit-unavailable-slots/', edit_unavailable_slots, name='edit_unavailable_slots'),
    path('barber/login/', auth_views.LoginView.as_view(template_name='barber_login.html'), name='barber_login'),
    path('booking/delete/<int:booking_id>/', delete_booking, name='delete_booking'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)