from blog.models import CarSales
import csv





def runCSV():
    with open(path) as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header
        CarSales.objects.all().delete()
        for row in reader:
            print(row)
            _, created = CarSales.objects.get_or_create(
                Manufacturer = row[0],
                Model = row[1],
                Sales_in_thousands = row[2],
                Price_in_thousands = row[3],
                Engine_size = row[4],
                Horsepower = row[5],
                Fuel_efficiency = row[6],
                
            )
            CarSales.save()