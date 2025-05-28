from django.db import models
from django.contrib.auth.models import User

class Barber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name="Name")
    experience = models.TextField(verbose_name="experience")
    photo = models.ImageField(upload_to='barbers/', verbose_name="photo")
    email = models.EmailField(blank=True,null=True)
    
    def __str__(self):
        return self.name

class Service(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE, related_name='services')
    service_name = models.CharField(max_length=100, verbose_name="Послуга")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")

    def __str__(self):
        return f"{self.service_name} - {self.price} грн"
    
class Booking(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    email = models.EmailField(max_length=255, blank=True,null=True)

    class Meta:
        unique_together = ('barber', 'date', 'time')
        
class UnavailableSlot(models.Model):
    barber = models.ForeignKey(Barber, on_delete=models.CASCADE)
    date = models.DateField()
    
    class Meta:
        unique_together = ('barber', 'date')