from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from accounts.models import *
# Create your views here.

def index(request):
    hotels = Hotel.objects.all()
    if request.GET.get('search'):
        hotels = hotels.filter(hotel_name__icontains = request.GET.get('search'))

    if request.GET.get('sort_by'):
        sort_by = request.GET.get('sort_by')
        if sort_by ==  "sort_low":
            hotels = hotels.order_by("hotel_offer_price")
        elif sort_by == "sort_high":
            hotels = hotels.order_by("hotel_offer_price")

    return render(request, 'index.html', context = {'hotels':hotels[:50]})

from datetime import datetime

def hotel_details(request, slug):
    # Retrieve the hotel object; consider using get_object_or_404 for better error handling.
    hotel = get_object_or_404(Hotel, hotel_slug=slug)

    if request.method == "POST":
        # Retrieve date strings from POST data.
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        # Validate that both dates are provided.
        if not start_date_str or not end_date_str:
            messages.warning(request, "Please provide both start and end dates.")
            return HttpResponseRedirect(request.path_info)

        try:
            # Convert the string dates to datetime objects.
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            messages.warning(request, "Dates must be in the format YYYY-MM-DD.")
            return HttpResponseRedirect(request.path_info)

        # Calculate the number of days between the dates.
        days_count = (end_date - start_date).days

        # Ensure the booking period is valid.
        if days_count <= 0:
            messages.warning(request, "Invalid Booking Date")
            return HttpResponseRedirect(request.path_info)

        # Create the booking record.
        HotelBooking.objects.create(
            hotel=hotel,
            booking_user=HotelUser.objects.get(id=request.user.id),
            booking_start_date=start_date,
            booking_end_date=end_date,
            price=hotel.hotel_offer_price * days_count
        )

        messages.success(request, "Booking Captured")
        return HttpResponseRedirect(request.path_info)

    return render(request, 'hotel_detail.html', context={'hotel': hotel})