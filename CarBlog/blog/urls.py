from django.urls import path, include
from . import view
from django.contrib.auth import views


from rest_framework import routers



urlpatterns = [
    path('', view.home, name='home'),
    path('home/', view.home, name='home'),
    
   # path("register/", view.register, name="register"),
    path('login/', view.user_login, name='login'),
    
    
    
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('resume/', view.resume, name='resume'),
    path('upload/', view.uploadForm, name='uploadForm'),
    path('Charts/', view.showCharts, name='showCharts'),
    path('Charts/<str:name>',view.show_Charts, name='show_Charts'),
    
    
    # post/ means that the URL should begin with the word post followed by a /. So far so good.
    # <int:pk> – this part is trickier. It means that Django expects an integer value and will transfer it to a view as a variable called pk.
    # /  then we need a / again before finishing the URL.
   # path('post/<int:pk>/', views.post_detail, name='post_detail'),
   # path('post/new/', views.post_new, name='post_new'),
   # path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
]
