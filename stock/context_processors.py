from django.db.models import F
from .models import Stock


def low_stock_alerts(request):
    """Counts active stock items that are at or below their low stock threshold."""
    alert_count = 0
    if request.user.is_authenticated:
        alert_count = Stock.objects.filter(quantity__lte=F('low_stock_threshold')).count()

    return {
        'low_stock_count': alert_count
    }
