from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from rest_framework import permissions
from catalog.models import City, Industry, Company, JobVacancy, Application


class VacancyIntegrationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_city = City.objects.create(name='test_city')
        cls.test_company_01 = Company.objects.create(name='test_company_01')
        cls.test_company_02 = Company.objects.create(name='test_company_01')
        cls.test_industry_01 = Industry.objects.create(name='test_industry_01')
        cls.test_vacancy_01 = JobVacancy.objects.create(
            title='test_vacancy_01',
            city=cls.test_city,
            company=cls.test_company_01,
            industry=cls.test_industry_01,
            years_of_exp='3-5',
            type='fulltime'
        )
        cls.test_vacancy_02 = JobVacancy.objects.create(
            title='test_vacancy_02',
            city=cls.test_city,
            company=cls.test_company_02,
            industry=cls.test_industry_01,
            years_of_exp='3-5',
            type='fulltime'
        )

    def test_get_vacancy_by_company(self):
        res_count = JobVacancy.objects.filter(company=1)
        self.assertEqual(len(res_count), 1)

    def test_get_vacancy_by_industry(self):
        res_count = JobVacancy.objects.filter(industry=1)
        self.assertEqual(len(res_count), 2)


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
        authenticated_user = User.objects.create(email='authenticated@gsmth.com', password='password03', is_staff=False)
        factory = RequestFactory()
        request = factory.post('/api/v1/applications')
        request.user = authenticated_user
        permission = permissions.IsAuthenticatedOrReadOnly()
        has_permission = permission.has_permission(request, None)
        self.assertTrue(has_permission)

    def test_admin_permisiion(self):
        admin_user = User.objects.create(email='admin@gsmth.com', password='password02', is_staff=True)
        factory = RequestFactory()
        request = factory.post('/api/v1/companies')
        request.user = admin_user
        permission = permissions.IsAdminUser()
        has_permission = permission.has_permission(request, None)
        self.assertTrue(has_permission)