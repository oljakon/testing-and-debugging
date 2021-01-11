from django.test import TestCase
from django.contrib.auth.models import User
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


