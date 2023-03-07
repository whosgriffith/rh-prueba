from rest_framework import viewsets, permissions, serializers
from rapihogar.models import Company
from api.serializers import CompanySerializer


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.filter()
