from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.conf import settings
from django.db import connection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from apps.users.models import TatarUser
import os


class BaseProjectTestCase(StaticLiveServerTestCase):
    fixtures = [os.path.join(os.path.join(os.path.dirname(__file__), 'fixtures'), 'tatar.json')]
    # Credentials for test user
    credentials = {'username': 'test_user',
                   'password': 'test_password',
                   'email': 'test@test.com'}

    @classmethod
    def setUpClass(cls):
        StaticLiveServerTestCase.setUpClass()
        with connection.cursor() as cursor:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS fuzzystrmatch")

    def setUp(self):
        TatarUser.objects.create_user(**self.credentials)


class SeleniumTestCase(BaseProjectTestCase):
    @classmethod
    def setUpClass(cls):
        BaseProjectTestCase.setUpClass()
        cls.driver = WebDriver(executable_path=settings.GECKODRIVER_PATH)

    def tearDown(self):
        self.driver.delete_all_cookies()

    def get_result_from_main_page(self, word: str, tag_id: str) -> str:
        """
        Move to main page, find twin for given 'word' there and return it

        tag_id parameter is for working both with right and incorrect requests
        """
        self.driver.get(self.live_server_url + reverse('home'))
        form = self.driver.find_element_by_id('id_word')
        form.send_keys(word)
        self.driver.find_element_by_id('gettatar').click()
        description = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, tag_id))
        )
        form.clear()
        return description.text

    def log_in(self):
        """
        Move to login page and log in with credentials provided above
        """
        self.driver.get(self.live_server_url + reverse('login'))
        username_form = self.driver.find_element_by_id('id_username')
        password_form = self.driver.find_element_by_id('id_password')
        username_form.send_keys(self.credentials['username'])
        password_form.send_keys(self.credentials['password'])
        self.driver.find_element_by_id('submit').click()