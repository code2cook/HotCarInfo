import csv
import logging
from django.shortcuts import render, get_object_or_404, redirect
# from .models import Post
import os

from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from blog.models import CarSales
from blog.serializers import CarsaleSerializer


from rest_framework import viewsets
from rest_framework import permissions
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, GroupSerializer


from django.utils import timezone
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import Group

from django.contrib.auth.forms import AuthenticationForm
from .processCSV import runCSV

from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import UploadForm
from django.views.generic.base import View

from django.shortcuts import render

from django.conf import settings

from django.http import HttpResponseRedirect

from django.contrib import messages

from .forms import DataImportForm









class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def post_list(request):
    # posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/base.html')


def home(request):
    return render(request, 'blog/home.html')


def resume(request):

    
    return render(request, 'blog/resume.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            if request.user.is_authenticated == False:
                login(request, user)
                messages.success(request, "Registration successful.")
            return redirect("/")
    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="blog/register.html", context={"register": form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return render(request=request, template_name="blog/login.html", context={'form': form})
    else:
        form = AuthenticationForm()

    return render(request=request, template_name="blog/login.html", context={'form': form})


        
        
def uploadForm(request):
    if "GET" == request.method:
        return render(request, "blog/upload.html")
    # if not GET, then proceed
    workpath = os.path.dirname(__file__)
    file_path = os.path.join(workpath, 'Car_sales.csv')
    #form = DataImportForm(request.POST, request.FILES)
    
    file = open(file_path)
    file_data = csv.reader(file)
    next(file_data)
    csv_file = request.FILES["csv_file"]

    if not csv_file.name.endswith('.csv'):
        messages.error(request,'File is not CSV type')
        return HttpResponseRedirect(reverse("uploadForm"))
    i = 0
    for line in file_data:	   
        
        new_data =CarSales.objects.create(
            Manufacturer = line[0],
            Model = line[1],
            Sales_in_thousands = line[2],
            Price_in_thousands = line[3],
            Engine_size = line[4],
            Horsepower = line[5],
            Fuel_efficiency = line[6],
        )
        i += 1
        try:
            new_data.save()
        except:
            print ("there was a problem with line", i)
        
        
        #print(CarSales.objects.filter(Manufacturer='Toyota'))
    
    carData = CarSales.objects.all()
    carData_python = list(carData.values())        
    return render(request, 'blog/upload.html', {'car':carData_python})

def showCharts(request):
    labels = []
    data = []

    queryset = CarSales.objects.order_by('Sales_in_thousands')[:5]
    
    for car in queryset:
        labels.append(car.Model)
        data.append(float(car.Sales_in_thousands))
        

    
    return render(request, 'blog/showCharts.html', {
        'labels': labels,
        'data': data,
    })
     
 
