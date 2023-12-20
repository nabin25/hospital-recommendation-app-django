from django.shortcuts import render,redirect,get_object_or_404
from .models import Hospital,UserResponse,Preference,Schedule
import folium
import geocoder
import requests
import openai
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from .forms import ScheduleForm, PreferenceForm
from django.contrib import messages
from django.http import HttpResponseBadRequest
import math
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm

openai.api_key = 'YOUR_API_KEY'

import openai
from .models import Hospital

def get_category(probable_disease):
    hospital_categories = Hospital.CAT
    categories_list = [cat[0] for cat in hospital_categories]
    prompt = f"Probable disease: {probable_disease}\nHospital specializations: {', '.join(categories_list)}\nRecommended category:"
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=5,
        temperature=0.1
    )

    recommended_category = response.choices[0].text.strip()
    return recommended_category


def get_probable_disease(gender, symptoms):
    prompt = f"Patient gender: {gender}\nSymptoms: {symptoms}\nProbable disease:"

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=5,
        temperature=2
    )

    probable_disease = response.choices[0].text.strip()
    return probable_disease


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = '/login'


def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))
    
    # Radius of the Earth in kilometers
    radius = 6371
    
    # Haversine formula
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance

@login_required
def index(request):
    return render(request, 'hosp_rec_app/index.html')

@login_required
def about(request):
    return render(request,'hosp_rec_app/about.html')

@login_required
def contact(request):
    return render(request,'hosp_rec_app/contact.html')

@login_required
def search(request):
    context = {
        'types':Hospital.TYPES,
        'cats':Hospital.CAT
    }
    return render(request,'hosp_rec_app/search.html',context)

@login_required
def search_by_sym(request):
    context = {
        'types':Hospital.TYPES,
    }
    return render(request,'hosp_rec_app/search_by_sym.html',context)

@login_required
def response_received(request):
    if request.method == "POST":
        name1 = request.POST.get('name')
        email1 = request.POST.get('email')
        message1 = request.POST.get('message')
        response = UserResponse(
            name = name1,
            email = email1,
            message = message1,
        )
        response.save()
        return render(request,'hosp_rec_app/resp_sub.html')

    return(request, 'hosp_rec_app/contact.html')

@login_required
def schedule(request):
    if request.method == "POST":
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            return redirect('schedule')
    else:
        item_list = Schedule.objects.filter(user=request.user)
        form = ScheduleForm()
        page = {
            "forms" : form,
            "list" : item_list,
            "title" : "SCHEDULE LIST",
        }
        return render(request,'hosp_rec_app/schedule.html',page)

@login_required
def preference(request):
    if request.method == "POST":
        form = PreferenceForm(request.POST)
        if form.is_valid():
            preference = form.save(commit=False)
            preference.user = request.user
            preference.save()
            return redirect('preferences')
    else:
        item_list = Preference.objects.filter(user=request.user)
        form = PreferenceForm()
        page = {
            "forms" : form,
            "list" : item_list,
            "title" : "PREFERENCE LIST",
        }
        return render(request,'hosp_rec_app/preference.html',page)
    
### function to remove item , it recive todo item id from url ##
@login_required
def remove(request, pk):
    item = Schedule.objects.get(id=pk)
    item.delete()
    messages.info(request,"Schedule removed !!!")
    return redirect('schedule')

@login_required
def pref_remove(request, pk):
    item = Preference.objects.get(id=pk)
    item.delete()
    messages.info(request,"Preference removed !!!")
    return redirect('preferences')


@login_required
def map_view(request):

    preferred_list = Preference.objects.filter(user=request.user)
    preferred_hosp_ids = preferred_list.values_list('preferred_hosp__hosId', flat=True)
    if request.method == "POST":
        location_type = request.POST.get('location_type')
        cat = request.POST.get('category')
        type = request.POST.get('type')
        radius = request.POST.get('radius')
        if location_type == 'Current_Address':
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
        else:
            location = request.POST.get('location') 
            geolocator = geocoder.osm(location)
            latitude = geolocator.lat
            longitude = geolocator.lng

        # create a folium map centered on the location
        map = folium.Map(location=[latitude, longitude], zoom_start=11)    
        # add a marker at the location
        folium.Marker(location=[latitude, longitude], tooltip="Here You are", popup="Your Location", icon=folium.Icon(color='blue')).add_to(map)

        hospitals = Hospital.objects.all()
        if type:
            hospitals = hospitals.filter(hosType=type)
        if cat:
            hospitals = hospitals.filter(hosSpec__contains=[cat])
        # print(hospitals)

        if preferred_list:
            preferred_hospitals = hospitals.filter(hosId__in=preferred_hosp_ids)
            remaining_hospitals = hospitals.exclude(hosId__in=preferred_hosp_ids)
            hospitals = list(preferred_hospitals) + list(remaining_hospitals)

        if radius and float(radius) != 0:
            filtered_hospitals = []

            for hospital in hospitals:
                distance = calculate_distance(latitude,longitude,hospital.hosLat,hospital.hosLong)
                if distance <= float(radius):
                    filtered_hospitals.append(hospital)

            hospitals = filtered_hospitals

        for hospital in hospitals:
            folium.Marker(location=[hospital.hosLat, hospital.hosLong], tooltip=hospital.hosName, popup=hospital.hosName, icon=folium.Icon(color='red')).add_to(map)
           
        return render(request, 'hosp_rec_app/map.html', {'map': map._repr_html_(), 'hospitals':hospitals,'latitude':latitude, 'longitude':longitude})
    
    return render(request, "hosp_rec_app/search.html",{ 'types':Hospital.TYPES,'cats':Hospital.CAT} )

@login_required
def sym_map_view(request):
    preferred_list = Preference.objects.filter(user=request.user)
    preferred_hosp_ids = preferred_list.values_list('preferred_hosp__hosId', flat=True)
    if request.method == "POST":
        print(request.POST)
        location_type = request.POST.get('location_type')
        symptoms = request.POST.get('symptoms')
        gender = request.POST.get('gender')
        type = request.POST.get('type')
        radius = request.POST.get('radius')
        if location_type == 'Current_Address':      
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
        else:
            location = request.POST.get('location') 
            geolocator = geocoder.osm(location)
            latitude = geolocator.lat
            longitude = geolocator.lng
        probable_disease = get_probable_disease(gender=gender, symptoms=symptoms)
        related_category = get_category(probable_disease=probable_disease)
        related_category = related_category.strip()
        cat = related_category
        # create a folium map centered on the location
        map = folium.Map(location=[latitude, longitude], zoom_start=11)    
        # add a marker at the location
        folium.Marker(location=[latitude, longitude], tooltip="Here You are", popup="Your Location", icon=folium.Icon(color='blue')).add_to(map)

        hospitals = Hospital.objects.all()
        if type:
            hospitals = hospitals.filter(hosType=type)
        # if cat:
        #     hospitals = hospitals.filter(hosSpec__contains=[cat])
        # print(hospitals)

        if preferred_list:
            preferred_hospitals = hospitals.filter(hosId__in=preferred_hosp_ids)
            remaining_hospitals = hospitals.exclude(hosId__in=preferred_hosp_ids)
            hospitals = list(preferred_hospitals) + list(remaining_hospitals)

        if radius and float(radius) != 0:
            filtered_hospitals = []

            for hospital in hospitals:
                distance = calculate_distance(latitude,longitude,hospital.hosLat,hospital.hosLong)
                if distance <= float(radius):
                    filtered_hospitals.append(hospital)

            hospitals = filtered_hospitals

        for hospital in hospitals:
            folium.Marker(location=[hospital.hosLat, hospital.hosLong], tooltip=hospital.hosName, popup=hospital.hosName, icon=folium.Icon(color='red')).add_to(map)
           
        return render(request, 'hosp_rec_app/map.html', {'map': map._repr_html_(), 'probable_disease':probable_disease, 'related_category':related_category, 'hospitals':hospitals, 'latitude':latitude, 'longitude':longitude})
    
    return render(request, "hosp_rec_app/search_by_sym.html",{ 'types':Hospital.TYPES,'cats':Hospital.CAT} )


def direction(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        if not all([id, latitude, longitude]):
            return HttpResponseBadRequest('Missing required parameters')
    else:
        return HttpResponseBadRequest('Invalid request method')

    hospital = Hospital.objects.get(hosId=id)
    start_point = (latitude, longitude)
    print(start_point)
    end_point = (hospital.hosLat, hospital.hosLong)
    url = 'https://api.openrouteservice.org/v2/directions/driving-car'
    params = {
        'api_key': 'Add your key from open route service',
        'start': f'{start_point[1]},{start_point[0]}',
        'end': f'{end_point[1]},{end_point[0]}',
    }
    response = requests.get(url, params=params).json()
    try:
        coordinates = response['features'][0]['geometry']['coordinates']
    except IndexError:
        return HttpResponseBadRequest('No route found')
    coordinates = [[c[1], c[0]] for c in coordinates]  # Convert coordinates to correct format
    map = folium.Map(location=start_point, zoom_start=14)
    folium.Marker(location=start_point, tooltip="Start").add_to(map)
    folium.Marker(location=end_point, tooltip="End").add_to(map)
    folium.PolyLine(coordinates, color='blue').add_to(map)
    return render(request, 'hosp_rec_app/direction.html', {'map': map._repr_html_()})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form}) 

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')