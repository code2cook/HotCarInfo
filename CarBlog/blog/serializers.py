from django.contrib.auth.models import User, Group
from rest_framework import serializers, viewsets
from blog.models import CarSales

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        

class CarsaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarSales
        fields = "__all__"
        

class CarsaleViewSet(viewsets.ModelViewSet):
    queryset = CarSales.objects.all()
    serializer_class = CarsaleSerializer
    