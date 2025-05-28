from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import PricingConfiguration
from datetime import datetime

@api_view(['POST'])
def calculate_price(request):
    data = request.data
    date = datetime.strptime(data['ride_date'], '%Y-%m-%d')
    day = date.strftime('%a').lower()
    distance = float(data['distance_km'])
    duration_hours = float(data['duration_hours'])
    waiting_minutes = int(data['waiting_minutes'])

    config = PricingConfiguration.objects.filter(applicable_days__code=day, is_active=True).first()

    if not config:
        return Response({"error": "No active config for this day."}, status=400)

    dbp = config.dbp.first()
    dap = config.dap.first()
    wc = config.wc.first()
    tmfs = config.tmf.all()

    d_price = dbp.price if distance <= dbp.max_distance_km else (
        dbp.price + ((distance - dbp.max_distance_km) * dap.price_per_km)
    )

    t_multiplier = 1
    for tmf in tmfs:
        if tmf.start_hour <= duration_hours < tmf.end_hour:
            t_multiplier = tmf.multiplier
            break

    t_price = duration_hours * t_multiplier * 1

    wait_charge = max(waiting_minutes - wc.free_minutes, 0) * wc.charge_per_min

    total_price = round(d_price + t_price + wait_charge, 2)

    return Response({"total_price": total_price})
