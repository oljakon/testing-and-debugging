from django.test import TestCase
from catalog.models import City, Industry, Company, JobVacancy, Application
from catalog.tests.unit_tests.user_builder import UserBuilder


class CityTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_city_01 = City.objects.create(name='test_city01')
        cls.test_city_02 = City.objects.create(name='test_city02')

    def test_get_city_by_name(self):
        test_city_01 = City.objects.get(name='test_city01')
        self.assertEqual(test_city_01.name, 'test_city01')

    def test_get_not_existing_city(self):
        throw_exception = False

        try:
            City.objects.get(name='test_city03')
        except City.DoesNotExist:
            throw_exception = True

        self.assertTrue(throw_exception)

    def test_update_city(self):
        City.objects.filter(name='old_test_city02').update(name='test_city02')
        self.test_city_02.refresh_from_db()
        self.assertEqual(self.test_city_02.name, 'test_city02')


class IndustryTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_industry_01 = Industry.objects.create(name='test_industry01')
        cls.test_industry_02 = Industry.objects.create(name='test_industry02')

    def test_get_industry_by_name(self):
        test_industry_01 = Industry.objects.get(name='test_industry01')
        self.assertEqual(test_industry_01.name, 'test_industry01')

    def test_get_not_existing_industry(self):
        throw_exception = False

        try:
            Industry.objects.get(name='test_industry03')
        except Industry.DoesNotExist:
            throw_exception = True

        self.assertTrue(throw_exception)

    def test_update_industry(self):
        Industry.objects.filter(name='old_test_industry02').update(name='test_industry02')
        self.test_industry_02.refresh_from_db()
        self.assertEqual(self.test_industry_02.name, 'test_industry02')


class CompanyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_company_01 = Company.objects.create(name='test_company01')
        cls.test_company_02 = Company.objects.create(name='test_company02')

        cls.test_industry_01 = Industry.objects.create(name='test_industry01')
        cls.test_industry_02 = Industry.objects.create(name='test_industry02')

        industry_object_1 = Industry.objects.filter(id=1)
        cls.test_company_01.industry.set(industry_object_1)
        cls.test_company_01.save()

        industry_objects = Industry.objects.all()
        cls.test_company_02.industry.set(industry_objects)
        cls.test_company_02.save()

    def test_get_company_by_name(self):
        test_company_01 = Company.objects.get(name='test_company01')
        self.assertEqual(test_company_01.name, 'test_company01')

    def test_get_not_existing_company(self):
        throw_exception = False

        try:
            Company.objects.get(name='test_company03')
        except Company.DoesNotExist:
            throw_exception = True

        self.assertTrue(throw_exception)

    def test_update_company(self):
        Company.objects.filter(name='old_test_company02').update(name='test_company02')
        self.test_company_02.refresh_from_db()
        self.assertEqual(self.test_company_02.name, 'test_company02')


class VacancyTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_company = Company.objects.create(name='test_vacancy')
        cls.test_industry = Industry.objects.create(name='test_vacancy')
        cls.test_city = City.objects.create(name='test_vacancy')
        cls.test_vacancy = JobVacancy.objects.create(
            title = 'test_vacancy',
            company = cls.test_company,
            industry = cls.test_industry,
            city=cls.test_city,
            years_of_exp = '3-5',
            type = 'fulltime'
        )

    def test_vacancy_company(self):
        test_vacancy = JobVacancy.objects.get(title='test_vacancy')
        self.assertIsInstance(test_vacancy.company, Company)

    def test_vacancy_industry(self):
        test_vacancy = JobVacancy.objects.get(title='test_vacancy')
        self.assertIsInstance(test_vacancy.industry, Industry)

    def test_vacancy_city(self):
        test_vacancy = JobVacancy.objects.get(title='test_vacancy')
        self.assertIsInstance(test_vacancy.city, City)

    def test_get_vacancy(self):
        test_vacancy_01 = JobVacancy.objects.get(title='test_vacancy')
        self.assertEqual(test_vacancy_01.title, 'test_vacancy')

    def test_get_not_existing_vacancy(self):
        throw_exception = False

        try:
            JobVacancy.objects.get(title='test_vacancy02')
        except JobVacancy.DoesNotExist:
            throw_exception = True

        self.assertTrue(throw_exception)


class ApplicationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_user_01 = UserBuilder('test_username01').with_password('test_password02').build()
        cls.test_vacancy = JobVacancy.objects.create(title='test_vacancy')
        cls.test_application = Application.objects.create(id=1, applicant=cls.test_user_01, job=cls.test_vacancy)

    def test_get_application(self):
        test_application = Application.objects.get(id=1)
        self.assertEqual(test_application.id, 1)

    def test_application_creation(self):
        test_application = Application.objects.get(id=1)
        self.assertIsInstance(test_application, Application)

    def test_get_not_existing_application(self):
        throw_exception = False

        try:
            Application.objects.get(id=2)
        except Application.DoesNotExist:
            throw_exception = True

        self.assertTrue(throw_exception)