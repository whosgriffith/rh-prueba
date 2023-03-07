from rest_framework import routers
from django.urls import path, include

from api.views import CompanyViewSet, RepairmanList, RepairmanSummary

router = routers.DefaultRouter()
router.register(r'company', CompanyViewSet, basename='company')

urlpatterns = [
    path('', include(router.urls)),
    path('repairman/', RepairmanList.as_view(), name="repairman"),
    path('repairman/summary/', RepairmanSummary.as_view(), name="repairman-summary"),
]
