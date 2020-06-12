from django.test import TestCase
from django.urls import reverse
from itertools import combinations_with_replacement
from .models import Tatar


class TatarTest(TestCase):
    fixtures = ['tatar.json']

    def test_results_are_always_determined(self):
        for word in combinations_with_replacement('абвгд', 5):
            results = set(Tatar.objects.find_twin(''.join(word)) for _ in range(10))
            self.assertEqual(len(results), 1, "Result must me determined")

    def test_hit_parameter_has_been_increased(self):
        start_hits = {}
        for word in Tatar.objects.top(5):
            start_hits[word] = word.hit
            self.client.get(reverse('home'), data={'word': word})
            self.assertEqual(Tatar.objects.get(word=word).hit - start_hits[word], 1, "No difference")

