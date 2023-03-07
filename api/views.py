from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from rapihogar.models import Company
from api.serializers import CompanySerializer
from api.services import RepairmanService


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.filter()


class RepairmanList(APIView):
    """
    List all repairman's with total pay.
    """
    def get(self, request):
        data = RepairmanService.get_list(request.query_params)
        return Response(data)


class RepairmanSummary(APIView):
    """
    Get a summary with data from all the repairman's.
    """
    def get(self, request):
        data = RepairmanService.get_summary()
        return Response(data)
