from django.shortcuts import render, get_object_or_404, redirect
# from .models import Post


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
