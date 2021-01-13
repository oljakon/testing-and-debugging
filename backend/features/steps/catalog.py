from behave import *
import requests
import json
from django.contrib.auth.models import User
from catalog.models import City, Industry, Company, JobVacancy, Application

use_step_matcher("re")

@given('registered user')
def set_impl(context):
    user_bdd = User.objects.create(username='user_bdd', email='email@bdd.com', password='password_bdd')
    user_bdd.save()

    context.url = context.base_url + '/api/v1/api-auth/login/'
    context.body = {
        'username': 'user_bdd',
        'password': 'password_bdd',
    }
    context.res = requests.post(context.url, data=json.dumps(context.body))


@given('job vacancy')
def set_impl(context):
    city_bdd = City.objects.create(name='city_bdd')
    company_bdd = Company.objects.create(name='company_bdd')
    industry_bdd = Industry.objects.create(name='industry_bdd')
    vacancy_bdd = JobVacancy.objects.create(
        title='vacancy_bdd',
        city=city_bdd,
        company=company_bdd,
        industry=industry_bdd,
        years_of_exp='3-5',
        type='fulltime'
    )
    vacancy_bdd.save()


@when('user creates an application to a job')
def set_impl(context):
    application_data = {
        'job': context.base_url + '/api/v1/vacancies/1/',
        'applied_on': '2021-01-01',
    }

    context.res = requests.post(context.base_url + '/api/v1/applications/', json=application_data)


@then('returns code 201')
def set_impl(context):
    assert context.res.status_code == 201