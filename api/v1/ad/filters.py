import django_filters as filters

from app.models import AdModel
class AdFilter(filters.FilterSet):
    price = filters.RangeFilter()
    # created_at = filters.DateTimeFilter()
    created_at = filters.DateFromToRangeFilter()


    class Meta:
        model = AdModel
        fields = ['price', 'created_at']