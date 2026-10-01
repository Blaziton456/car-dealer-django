from django.db import models


class DealerReview(models.Model):
    dealer_id = models.IntegerField()
    dealership = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    purchase = models.BooleanField(default=False)
    review = models.TextField()
    purchase_date = models.CharField(max_length=20)
    car_make = models.CharField(max_length=100)
    car_model = models.CharField(max_length=100)
    car_year = models.IntegerField()
    sentiment = models.CharField(max_length=20, default="Positive")

    def __str__(self):
        return self.review

class Dealer(models.Model):
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zip = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)

    def __str__(self):
        return self.full_name