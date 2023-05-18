import django_filters
from django.contrib.auth import get_user_model


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = get_user_model()
        fields = ["email"]
