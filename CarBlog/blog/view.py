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

import pandas as pd









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
    data = {}
    if "GET" == request.method:
        return render(request, "blog/upload.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return render(request, 'blog/upload.html',context={'csv_data': "this is not an csv file"})
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("blog/upload.html"))
        
        try:
            df = pd.read_csv(csv_file,encoding='ISO-8859-1')
            csv_data = pd.DataFrame(data=df)
            table_data = csv_data.to_html() 
            return render(request, 'blog/upload.html',context={'csv_data': table_data})
        except:
            return render(request, 'blog/upload.html',context={'csv_data': "this csv file has no header please upload csv file with header"})


    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return render(request, 'blog/upload.html',context={'csv_data': table_data})

def show_Charts(request,name):
    labels = []
    data = []
    if name == "most_car_sold":
        queryset = CarSales.objects.order_by('Sales_in_thousands')[:5]

    elif name == "most_expensive_sold":
        queryset = CarSales.objects.order_by('Price_in_thousands')[:5]
    
    elif name == "most_fuel_effiction":
        queryset = CarSales.objects.order_by('Fuel_efficiency')[:5]
        
    for car in queryset:
        labels.append(car.Model)
        data.append(float(car.Sales_in_thousands))
        
    return render(request, 'blog/showCharts.html', {
        'labels': labels,
        'data': data,
    })
        
    


def showCharts(request):
  
    if "GET" == request.method:
       # print("this is the name {}".format(name))
        return render(request, "blog/showCharts.html")
    elif "POST" == request.method:
        return render(request, "blog/showCharts.html")
