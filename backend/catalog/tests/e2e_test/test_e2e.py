from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import City, Industry, Company, JobVacancy, Application


class EndToEndTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.test_city_new = City.objects.create(name='test_city_new')
        cls.test_company_new = Company.objects.create(id=3, name='test_company_new')
        cls.test_industry_new = Industry.objects.create(id=3,name='test_industry_new')
        cls.test_vacancy_new = JobVacancy.objects.create(
            id=3,
            title='test_vacancy_new',
            city=cls.test_city_new,
            company=cls.test_company_new,
            industry=cls.test_industry_new,
            years_of_exp='3-5',
            type='fulltime'
        )
        cls.passed = 0

    def __get(self, model_class):
        return model_class.objects.all().first()

    def get_user(self):
        return self.__get(User)

    def get_vacancy(self):
        return self.__get(JobVacancy)

    def get_application(self):
        return self.__get(Application)

    def test_create_post_and_dislike(self):
        n = 100

        for _ in range(n):
            user_data = {
                'username': 'user',
                'email': 'user@smth.com',
                'password': 'password',
            }

            response = self.client.post('/api/v1/users/', data=user_data)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(self.get_user().username, 'user')

            self.client.force_login(self.get_user())
            user = response.json()['url']

            response = self.client.get('/api/v1/vacancies/')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/api/v1/vacancies/?company=3&industry=3')
            self.assertEqual(response.status_code, 200)

            response = self.client.get('/api/v1/vacancies/3/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(self.get_vacancy().title, 'test_vacancy_new')
            job = response.json()['url']

            application_data = {
                'applicant': user,
                'job': job,
                'applied_on': '2021-01-01',
            }

            response = self.client.post('/api/v1/applications/', data=application_data)
            self.assertEqual(response.status_code, 201)
            self.assertEqual(self.get_application().job.title, 'test_vacancy_new')
            application = response.json()['url']
            application_id = application[application[:-1].rfind('/') + 1:-1]

            response = self.client.delete(f'/api/v1/applications/{application_id}/')
            self.assertEqual(response.status_code, 204)

            User.objects.all().delete()

            self.passed += 1

    def tearDown(self):
        print('Passed: %d' % self.passed)