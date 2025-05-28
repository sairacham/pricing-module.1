from django.db import models
from django.contrib.auth.models import User

DAYS_OF_WEEK = [
    ('mon', 'Monday'), ('tue', 'Tuesday'), ('wed', 'Wednesday'),
    ('thu', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday'),
]

class PricingConfiguration(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    applicable_days = models.ManyToManyField('DayOfWeek')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DayOfWeek(models.Model):
    code = models.CharField(max_length=3, choices=DAYS_OF_WEEK, unique=True)

class DistanceBasePrice(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE, related_name='dbp')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    max_distance_km = models.FloatField()

class DistanceAdditionalPrice(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE, related_name='dap')
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)

class TimeMultiplierFactor(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE, related_name='tmf')
    start_hour = models.FloatField()
    end_hour = models.FloatField()
    multiplier = models.FloatField()

class WaitingCharge(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE, related_name='wc')
    charge_per_min = models.DecimalField(max_digits=10, decimal_places=2)
    free_minutes = models.PositiveIntegerField(default=3)

class PricingChangeLog(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.SET_NULL, null=True)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    change_summary = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
