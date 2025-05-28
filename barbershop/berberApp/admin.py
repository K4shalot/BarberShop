from django.contrib import admin
from .models import Barber,Service,Booking,UnavailableSlot
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class UnavailableSlotAdmin(admin.ModelAdmin):
    list_display = ('barber', 'date')
    list_filter = ('barber', 'date')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        if hasattr(request.user, 'barber'):
            return queryset.filter(barber=request.user.barber)
        return queryset.none()


class BarberAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'experience', 'email')
    search_fields = ['name', 'user__username']

    def save_model(self, request, obj, form, change):
        if not obj.user:
            user = User.objects.create(username=obj.name.lower(), email=obj.email)
            obj.user = user
        super().save_model(request, obj, form, change)

admin.site.register(Barber,BarberAdmin)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(UnavailableSlot, UnavailableSlotAdmin)

