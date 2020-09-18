from typing import Tuple
from .utils import SeleniumTestCase
from django.urls import reverse


class HistoryTest(SeleniumTestCase):
    def create_entry(self) -> Tuple[str, str]:
        word = self.get_result_from_main_page('слово', 'description')
        self.driver.get(self.live_server_url + reverse('show_history'))
        row = ''.join([e.text for e in self.driver.find_elements_by_tag_name('td')])
        return word, row

    def test_create_entry_and_find_it_in_history_page_when_not_logged(self):
        word, row = self.create_entry()
        self.assertIn(word, row)

    def test_create_entry_and_find_it_in_history_page_when_logged(self):
        self.log_in()
        word, row = self.create_entry()
        self.assertIn(word, row)

    def test_history_page_is_empty_at_starters(self):
        self.driver.get(self.live_server_url + reverse('show_history'))
        self.assertEqual(len(self.driver.find_elements_by_tag_name('td')), 0, 'History page is not empty')

