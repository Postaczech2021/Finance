from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, default=1)
    is_income = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Income(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True,editable=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)

class Outcome(models.Model):
    name = models.CharField(max_length=100)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True,editable=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)

