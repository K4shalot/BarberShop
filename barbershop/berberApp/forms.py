from django import forms
from .models import Booking
import datetime
from .models import UnavailableSlot

class BookingForm(forms.ModelForm):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    max_day = today + datetime.timedelta(days=10)
    
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'min': tomorrow.isoformat(),
                'max': max_day.isoformat()
            }
        ),
        initial=tomorrow,
    )
    time = forms.ChoiceField(
        choices=[(f"{hour:02d}:00", f"{hour:02d}:00") for hour in range(10, 20)],
        help_text="Виберіть годину"
    )

    class Meta:
        model = Booking
        fields = ['name', 'phone', 'email', 'barber', 'service', 'date', 'time']

    def clean(self):
        cleaned_data = super().clean()
        barber = cleaned_data.get("barber")
        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        
        if date and date < datetime.date.today() + datetime.timedelta(days=1):
            self.add_error("date", "Запис модливий лише з завтранього дня або пізніше.")
        
        if date and date.weekday() == 6:
            self.add_error("date", "Вибір неділі недоступний, оскільки це вихідний день.")

        if date and date < datetime.date.today():
            self.add_error("date", "Неможливо обрати дату в минулому.")

        if barber and date and time:
            if Booking.objects.filter(barber=barber, date=date, time=time).exists():
                self.add_error("time", "Цей час вже зайнятий. Оберіть інший.")
        
        if barber and date:
            if UnavailableSlot.objects.filter(barber=barber, date=date).exists():
                self.add_error("date", "Барбер недоступний у цей день.")
                
class UnavailableSlotForm(forms.Form):
    unavailable_dates = forms.CharField(
        widget=forms.TextInput(attrs={
            'id': 'id_unavailable_dates',
            'placeholder': 'Оберіть дні, коли ви недоступні'
        }),
        label="Оберіть дні, коли ви недоступні"
    )