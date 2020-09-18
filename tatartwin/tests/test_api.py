from .utils import BaseProjectTestCase
from django.urls import reverse
from rest_framework import status


class APITest(BaseProjectTestCase):

    def send_data_for_creation(self):
        data = {'word': 'пример',
                'translations': [
                    {
                        'translation': 'пример',
                        'examples': [
                            {
                                'example': 'ПримерНаТатарском1 - ПереводНаРусском1',
                            },
                            {
                                'example': 'ПримерНаТатарском2 - ПереводНаРусском2',
                            }

                        ]
                    }]
                }
        response = self.client.post(reverse('create'), content_type='application/json', data=data)
        return response

    def test_api_find_word_similar_to_entered(self):
        response = self.client.get(reverse('twin', kwargs={'word': 'двойник'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK, 'Response for api "twin" is not as expected')
        response = self.client.get(reverse('twin', kwargs={'word': 'dvoinik'}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, 'Response for api "twin" is not as expected')

    def test_api_find_top_words(self):
        response = self.client.get(reverse('top', kwargs={'number': 5}))
        self.assertEqual(len(response.data), 5, 'Response for api "top" is not as expected')
        for word in response.data:
            self.assertEqual(word.keys(), {'word', 'hit'}, 'Response for api "top" is not as expected')

    def test_create_tatar_word_when_logged(self):
        self.client.login(**self.credentials)
        response = self.send_data_for_creation()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_tatar_word_when_not_logged(self):
        response = self.send_data_for_creation()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)