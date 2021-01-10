from .models import Industry, Company, JobVacancy, Application, City
from rest_framework import permissions, viewsets

from .serializers import CitySerializer, CompanySerializer, IndustrySerializer, VacancySerializer, ApplicationSerializer

class CitiesAPIView(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CompaniesAPIView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class IndustriesAPIView(viewsets.ModelViewSet):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class VacanciesAPIView(viewsets.ModelViewSet):
    queryset = JobVacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = ('company', 'industry')


class ApplicationsAPIView(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filterset_fields = ('applicant', 'job')
