'''import os
import django
from django.test.runner import DiscoverRunner
from django.test.testcases import TestCase

os.environ['DJANGO_SETTINGS_MODULE'] = 'backend.settings'


def before_all(context):
    import django
    django.setup()
    from django.contrib.auth.models import User
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.old_db_config = context.test_runner.setup_databases()


def after_all(context):
    context.test_runner.teardown_databases(context.old_db_config)
    context.test_runner.teardown_test_environment()


def before_scenario(context, scenario):
    context.test = TestCase()
    context.test.setUpClass()


def after_scenario(context, scenario):
    context.test.tearDownClass()
    del context.test


def django_ready(context):
    context.django = True'''

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def wait(self, until, who=None, timeout=30, step=0.1):
    if who is None:
        who = self.driver
    return WebDriverWait(who, timeout, step).until(until)


def before_all(context):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    context.browser = webdriver.Chrome('/Users/olga/Documents/chromedriver', chrome_options=chrome_options)
    context.browser.implicitly_wait(1)
    context.server_url = 'http://localhost:8000'


def after_all(context):
    context.browser.quit()


def before_feature(context, feature):
    pass