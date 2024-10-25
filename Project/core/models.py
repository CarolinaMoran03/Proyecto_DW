from django.db import models

# Create your models here.

class Company(models.Model):
    description = models.CharField(max_length=255, null=False, blank=False)
    photo = models.ImageField(upload_to='img/')
    def __str__(self):
        return f"{self.description}"

class Position(models.Model):
    description = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return f"{self.description}"

class Country(models.Model):
    description = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return f"{self.description}"
  
class Province(models.Model):
    description = models.CharField(max_length=255, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.description}"    
    
class City(models.Model):
    description = models.CharField(max_length=255, null=False, blank=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=500, null=False, blank=False)
    def __str__(self):
        # Manejar casos en los que province o country puedan ser None
        if self.province and self.province.country:
            return f"{self.description}, {self.province.description}, {self.province.country.description}"
        elif self.province:
            return f"{self.description}, {self.province.description}"
        else:
            return f"{self.description}"

