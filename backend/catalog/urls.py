from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('companies', views.CompaniesAPIView)
router.register('industries', views.IndustriesAPIView)
router.register('vacancies', views.VacanciesAPIView)
router.register('cities', views.CitiesAPIView)
router.register('applications', views.ApplicationsAPIView)
router.register('users', views.UserViewSet)

urlpatterns = router.urls

