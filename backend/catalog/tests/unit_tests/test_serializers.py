from django.test import TestCase
from unittest.mock import MagicMock
from django.test.client import RequestFactory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from catalog.models import City, Industry, Company, JobVacancy, Application
from catalog.serializers import CitySerializer, CompanySerializer, IndustrySerializer, VacancySerializer, ApplicationSerializer

