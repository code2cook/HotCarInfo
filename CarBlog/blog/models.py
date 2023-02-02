from django.db import models

# Create your models here.

from django.db import models

class CarSales(models.Model):
    SaleId = models.AutoField(primary_key=True)
    Manufacturer = models.CharField(max_length = 20)
    Model = models.CharField(max_length = 20)
    Sales_in_thousands = models.DecimalField(decimal_places = 2, max_digits= 6)
    Price_in_thousands = models.DecimalField(decimal_places = 2, max_digits= 6)
    Engine_size = models.DecimalField(decimal_places = 2, max_digits=6)
    Horsepower = models.IntegerField()
    Fuel_efficiency = models.IntegerField()
    
    def __str__(self):
        return ('this {model} is made from{manufac} with price of {price}'.format(manufac=self.Manufacturer, model=self.Model, price=self.Price_in_thousands))
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=16)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    
    