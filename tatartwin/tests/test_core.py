from django.urls import reverse
from .utils import SeleniumTestCase


class TatarTest(SeleniumTestCase):
    def test_results_are_always_determined_when_not_logged(self):
        for word in ('слово', 'арка', 'дом'):
            results = set()
            for _ in range(3):
                tatar_word = self.get_result_from_main_page(word, 'description')
                results.add(tatar_word)
            self.assertEqual(len(results), 1, "Result must me determined")

    def test_results_are_always_determined_when_logged(self):
        self.log_in()
        for word in ('автошәһәр', 'аждаһа', 'азәрбайҗан'):
            results = set()
            for _ in range(3):
                tatar_word = self.get_result_from_main_page(word, 'description')
                results.add(tatar_word)
            self.assertEqual(len(results), 1, "Result must me determined")

    def test_hit_parameter_has_been_increased(self):
        self.driver.get(self.live_server_url + reverse('show_top'))
        word = self.driver.find_element_by_tag_name('h1').text
        num_of_hits_initial = int(self.driver.find_element_by_id('num_of_hits').text)
        self.driver.get(self.live_server_url + reverse('home'))
        self.get_result_from_main_page(word, 'description')
        self.driver.get(self.live_server_url + reverse('show_top'))
        num_of_hits_new = int(self.driver.find_element_by_id('num_of_hits').text)
        self.assertEqual(num_of_hits_new - num_of_hits_initial, 1, "No difference")

    def test_errors_info_appears_properly(self):
        for word in ('ROAR', 'автошәһәр'):
            error = self.get_result_from_main_page(word, 'errors')
            page = self.driver.find_element_by_tag_name('html').text
            self.assertIn(error, page)
        self.log_in()
        error = self.get_result_from_main_page('ROAR', 'errors')
        page = self.driver.find_element_by_tag_name('html').text
        self.assertIn(error, page)
