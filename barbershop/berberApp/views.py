from django.shortcuts import render, redirect, get_object_or_404
from .models import Barber, Booking, UnavailableSlot
from .forms import BookingForm, UnavailableSlotForm
from datetime import datetime
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from premailer import transform
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


load_dotenv()

def main_view(request):
    barbers = Barber.objects.all()
    for barber in barbers:
        barber.services_list = barber.services.all()
    return render(request, 'main.html', {'barbers': barbers})

def booking(request):
    barber_id = request.GET.get('barber')
    barber = Barber.objects.filter(id=barber_id).first() if barber_id else None

    if request.method == 'POST':
        form = BookingForm(request.POST)
    else:
        form = BookingForm(initial={'barber': barber})

    services = barber.services.all() if barber else []
    time_slots = [f"{h:02d}:00" for h in range(10, 20)]

    selected_date_str = form.data.get('date')
    try:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        selected_date = datetime.today().date()

    occupied_times_qs = Booking.objects.filter(barber=barber, date=selected_date).values_list('time', flat=True)
    occupied_times = [t.strftime('%H:%M') for t in occupied_times_qs if t]

    if request.method == 'POST' and form.is_valid():
        booking = form.save()

        user_name = booking.name
        phone = booking.phone
        email = booking.email
        service = booking.service.service_name
        price = booking.service.price
        barber_name = booking.barber.name
        time = booking.time.strftime('%H:%M')
        date = booking.date.strftime('%Y-%m-%d')

        # === Надсилання email клієнту (HTML + plain text) ===
        subject_client = 'Ви записались у наш Барбершоп!'
        message_client = (
            f"Послуга: {service}\n"
            f"Ціна: {price} ₴\n"
            f"Барбер: {barber_name}\n"
            f"Дата: {date}\n"
            f"Час: {time}"
        )

        html_content = render_to_string('booking_confirmation.html', {
            'service': service,
            'price': price,
            'barber': barber_name,
            'date': date,
            'time': time,
        })
        html_content = transform(html_content)

        email_msg = EmailMultiAlternatives(
            subject=subject_client,
            body=message_client,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
        email_msg.attach_alternative(html_content, "text/html")
        try:
            email_msg.send()
        except Exception as e:
            print(f"Error sending client HTML email: {e}")

        subject_admin = 'Новий запис у барбершопі'
        message_admin = (
            f"Ім’я клієнта: {user_name}\n"
            f"Номер телефону: {phone}\n"
            f"Email: {email}\n"
            f"Послуга: {service}\n"
            f"Ціна: {price} ₴\n"
            f"Барбер: {barber_name}\n"
            f"Дата: {date}\n"
            f"Час: {time}"
        )

        try:
            send_mail(subject_admin, message_admin, settings.EMAIL_HOST_USER, [os.getenv('EMAIL_LOGIN')])
        except Exception as e:
            print(f"Error sending admin email: {e}")

        return redirect('success')

    context = {
        'form': form,
        'barber_name': barber.name if barber else None,
        'barber': barber,
        'time_slots': time_slots,
        'occupied_times': occupied_times,
        'services': services,
    }

    return render(request, 'booking.html', context)



def success(request):
    return render(request, 'success.html')

def get_available_times(request):
    selected_date = request.GET.get('date')
    barber_id = request.GET.get('barber')

    if not selected_date:
        return JsonResponse({'error': 'Date is required'}, status=400)

    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    if selected_date.weekday() == 6:
        return JsonResponse({'available_times': []})

    if barber_id:
        barber = Barber.objects.get(id=barber_id)
        if UnavailableSlot.objects.filter(barber=barber, date=selected_date).exists():
            return JsonResponse({'available_times': []})
        occupied_times_qs = Booking.objects.filter(barber=barber, date=selected_date)
    else:
        occupied_times_qs = Booking.objects.filter(date=selected_date)

    occupied_times = [t.strftime('%H:%M') for t in occupied_times_qs.values_list('time', flat=True)]

    all_times = [f"{hour:02d}:00" for hour in range(10, 20)]

    available_times = [time for time in all_times if time not in occupied_times]

    return JsonResponse({'available_times': available_times})

@login_required
def barber_dashboard(request):
    barber = request.user.barber
    bookings = Booking.objects.filter(barber=barber).order_by('-date', '-time')
    return render(request, 'barber_dashboard.html', {'bookings': bookings})

@login_required
def edit_unavailable_slots(request):
    barber = request.user.barber
    if request.method == 'POST':
        form = UnavailableSlotForm(request.POST)
        if form.is_valid():
            dates_str = form.cleaned_data['unavailable_dates']
            date_list = dates_str.split(',')

            for date_str in date_list:
                date_str = date_str.strip()
                if date_str:
                    UnavailableSlot.objects.get_or_create(barber=barber, date=date_str)

            return redirect('barber_dashboard')
    else:
        form = UnavailableSlotForm()

    return render(request, 'edit_unavailable_slots.html', {'form': form})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if booking.barber.user == request.user:
        booking.delete()
    
    return redirect('barber_dashboard')