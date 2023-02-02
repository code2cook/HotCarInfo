from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from django.forms import FileField, Form, ModelForm
from .models import Product


class NewUserForm(UserCreationForm):

	class Meta:
		model = User
		fields = ("username", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		if commit:
			user.is_staff=True
			user.save()
		return user

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "sku", "price", "description"]
        
class UploadForm(Form):
    products_file = FileField()
    
class DataImportForm(forms.Form):
    file = forms.FileField()