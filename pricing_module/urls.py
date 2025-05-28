from django.contrib import admin
from django.urls import path
from pricing.views import calculate_price
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/calculate_price/', calculate_price),
    path('', RedirectView.as_view(url='/admin/')),
]
