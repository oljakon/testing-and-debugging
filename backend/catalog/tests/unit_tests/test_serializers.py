from django.test import TestCase
from unittest.mock import MagicMock
from django.contrib.auth.models import User
from catalog.models import City, Industry, Company, JobVacancy, Application
from catalog.serializers import CitySerializer, CompanySerializer, IndustrySerializer, VacancySerializer, \
    ApplicationSerializer, UserSerializer


class CitySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_city = City.objects.create(name='test_vacancy')
        cls.test_city_serializer = CitySerializer(cls.test_city, context={'request': MagicMock()})

    def test_included_fields(self):
        data = self.test_city_serializer.data
        self.assertEqual(set(data.keys()), {'url', 'name'})

    def test_city_field_content(self):
        data = self.test_city_serializer.data
        self.assertEqual(data['name'], 'test_vacancy')

    def test_update_name_field(self):
        self.test_city_serializer.update(self.test_city, {'name': 'test_city_new'})
        self.test_city.refresh_from_db()
        self.assertEqual(self.test_city.name, 'test_city_new')


class IndustrySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_industry = Industry.objects.create(name='test_vacancy')
        cls.test_industry_serializer = IndustrySerializer(cls.test_industry, context={'request': MagicMock()})

    def test_included_fields(self):
        data = self.test_industry_serializer.data
        self.assertEqual(set(data.keys()), {'url', 'name'})

    def test_industry_field_content(self):
        data = self.test_industry_serializer.data
        self.assertEqual(data['name'], 'test_vacancy')

    def test_update_name_field(self):
        self.test_industry_serializer.update(self.test_industry, {'name': 'test_industry_new'})
        self.test_industry.refresh_from_db()
        self.assertEqual(self.test_industry.name, 'test_industry_new')


class CompanySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_company = Company.objects.create(name='test_vacancy')
        cls.test_industry = Industry.objects.create(name='test_industry01')
        industry_object = Industry.objects.filter(id=1)
        cls.test_company.industry.set(industry_object)
        cls.test_company.save()
        cls.test_company_serializer = CompanySerializer(cls.test_company, context={'request': MagicMock()})

    def test_included_fields(self):
        data = self.test_company_serializer.data
        self.assertEqual(set(data.keys()), {'url', 'name', 'industry'})

    def test_company_field_content(self):
        data = self.test_company_serializer.data
        self.assertEqual(data['name'], 'test_vacancy')

    def test_update_name_field(self):
        self.test_company_serializer.update(self.test_company, {'name': 'test_company_new'})
        self.test_company.refresh_from_db()
        self.assertEqual(self.test_company.name, 'test_company_new')


class VacancySerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_city = City.objects.create(name='test_city')
        cls.test_company = Company.objects.create(name='test_company')
        cls.test_industry = Industry.objects.create(name='test_industry')
        cls.test_vacancy = JobVacancy.objects.create(title='test_vacancy', city=cls.test_city, company=cls.test_company,
                                                     industry=cls.test_industry, years_of_exp='3-5', type='fulltime')
        cls.test_vacancy_serializer = VacancySerializer(cls.test_vacancy, context={'request': MagicMock()})

    def test_included_fields(self):
        data = self.test_vacancy_serializer.data
        self.assertEqual(set(data.keys()), {'url', 'title', 'company', 'industry', 'city', 'years_of_exp', 'type'})

    def test_title_field_content(self):
        data = self.test_vacancy_serializer.data
        self.assertEqual(data['title'], 'test_vacancy')

    def test_update_title_field(self):
        self.test_vacancy_serializer.update(self.test_vacancy, {'title': 'test_vacancy_new'})
        self.test_vacancy.refresh_from_db()
        self.assertEqual(self.test_vacancy.title, 'test_vacancy_new')


class ApplicationSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='test_username', password='test_password')
        cls.test_city = City.objects.create(name='test_city')
        cls.test_company = Company.objects.create(name='test_company')
        cls.test_industry = Industry.objects.create(name='test_industry')
        cls.test_vacancy = JobVacancy.objects.create(title='test_vacancy', city=cls.test_city, company=cls.test_company,
                                                     industry=cls.test_industry, years_of_exp='3-5', type='fulltime')
        cls.test_application = Application.objects.create(applicant=cls.test_user, job=cls.test_vacancy, applied_on='2021-01-01')
        cls.test_application_serializer = ApplicationSerializer(cls.test_application, context={'request': MagicMock()})

    def test_included_fields(self):
        data = self.test_application_serializer.data
        self.assertEqual(set(data.keys()), {'url', 'applicant', 'job', 'applied_on'})

    def test_applicant_field_content(self):
        data = self.test_application_serializer.data
        self.assertEqual(data['applicant'], self.test_user.id)

    def test_applications_count_by_user(self):
        res_count = Application.objects.filter(applicant=self.test_user.id)
        self.assertEqual(len(res_count), 1)


class UserSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(username='test_username', email='test_email', password='test_password')
        cls.test_user_serializer = UserSerializer(cls.test_user, context={'request': MagicMock()})

    def test_contains_expected_fields(self):
        data = self.test_user_serializer.data
        self.assertEqual(set(data.keys()), {'url', 'username', 'email'})

    def test_username_field_content(self):
        data = self.test_user_serializer.data
        self.assertEqual(data['username'], 'test_username')

    def test_update_email_field(self):
        self.test_user_serializer.update(self.test_user, {'email': 'test_email_new'})
        self.test_user.refresh_from_db()
        self.assertEqual(self.test_user.email, 'test_email_new')