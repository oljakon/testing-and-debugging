from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from rest_framework import permissions
from catalog.models import City, Industry, Company, JobVacancy, Application
from catalog.views import ApplicationsAPIView, CompaniesAPIView


class ApplyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create(id=4, username='test_username', email='test_email', password='test_password')
        cls.test_city = City.objects.create(name='test_city')
        cls.test_company = Company.objects.create(name='test_company')
        cls.test_industry = Industry.objects.create(name='test_industry')
        cls.test_vacancy = JobVacancy.objects.create(id=4,title='test_vacancy', city=cls.test_city, company=cls.test_company,
                                                     industry=cls.test_industry, years_of_exp='3-5', type='fulltime')

    def test_apply(self):
        self.client.force_login(self.test_user)

        application_data = {
            'applicant': '/api/v1/users/4/',
            'job': '/api/v1/vacancies/4/',
            'applied_on': '2021-01-01',
        }

        response = self.client.post('/api/v1/applications/', data=application_data)
        self.assertEqual(response.status_code, 201)


class RegistrationTest(TestCase):
    def test_registration_success(self):
        user_data = {
            'username': 'username',
            'email': 'username@smth.com',
            'password': 'password',
        }

        response = self.client.post('/api/v1/users/', data=user_data)
        try:
            created_user = User.objects.get(username=user_data['username'])
            user_created = True
        except User.DoesNotExist:
            created_user = {'email': None}
            user_created = False

        self.assertEqual(response.status_code, 201)
        self.assertTrue(user_created)
        self.assertEqual(created_user.email, user_data['email'])


class PermissionTest(TestCase):
    def test_authenticated_permisiion(self):
        authenticated_user = User.objects.create(email='authenticated@smth.com', password='password03', is_staff=False)
        factory = RequestFactory()
        request = factory.post('/api/v1/applications')
        request.user = authenticated_user
        permission = permissions.IsAuthenticatedOrReadOnly()
        has_permission = permission.has_permission(request, ApplicationsAPIView)
        self.assertTrue(has_permission)

    def test_admin_permisiion(self):
        admin_user = User.objects.create(email='admin@smth.com', password='password02', is_staff=True)
        factory = RequestFactory()
        request = factory.post('/api/v1/companies')
        request.user = admin_user
        permission = permissions.IsAdminUser()
        has_permission = permission.has_permission(request, CompaniesAPIView)
        self.assertTrue(has_permission)

    def test_user_has_no_permisiion(self):
        authenticated_user_02 = User.objects.create(email='authenticate02d@smth.com', password='password03', is_staff=False)
        factory = RequestFactory()
        request = factory.post('/api/v1/companies')
        request.user = authenticated_user_02
        permission = permissions.IsAdminUser()
        has_permission = permission.has_permission(request, CompaniesAPIView)
        self.assertFalse(has_permission)