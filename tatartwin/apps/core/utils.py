"""
Functions for handling with history entries and fetching tatar words
"""
from django.utils import timezone
from .models import Tatar, History
from django.core.cache import cache
from django_redis import get_redis_connection


def get_tatar_twin(form):
    """
    Given a Form object, extract the initial word and get similar tatar word

    When fetched, word is set in the cache (Redis) for 5 minutes and in next same request it will be found in cache
    """
    word = form.cleaned_data['word']
    tatar_word = cache.get(word)
    if not tatar_word:
        tatar_word = Tatar.objects.find_twin(word)
        cache.set(word, tatar_word, 300)
    tatar_word.hit_increment()
    return word, tatar_word


def set_entry(request, tatar_word, word, response):
    """
    Given a tatar word and initial word, set the history entry

    The method of setting the entry depends on user's authentication status.
    If user is authenticated, insert entry in database.
    Otherwise, insert entry in cache server for 1 minute, using cookie

    To identify anonymous user's entry, following technique is used:
    First, we set 'first accessed' cookie, which is timestamp for user's first word request
    Then, set representation of the entry, in a key-value format. Value is tuple of tatar word, initial word,
    and moment of fetching tatar word 'now'(datetime object).
    Key is string, which format is 'h_timestamp:{first_accessed}:{now}', where 'first_accessed' and 'now'
    are objects described earlier. The pair is stored in the cache server (Redis).

    """
    if request.user.is_authenticated:
        History.objects.create(user=request.user, tatar_word=tatar_word, word=word)
    else:

        now = timezone.now()
        first_accessed = request.COOKIES.get('first_accessed', str(now))
        response.set_cookie('first_accessed', first_accessed)
        # Set entry for 1 minute
        cache.set(f'h_timestamp:{first_accessed}:{now}', (tatar_word, word, now), 60)


def get_all_entries(request):
    """
    Get all history entries for a user

    If he is authenticated, get entries in database
    Otherwise, find them in cache

    """
    pairs = []  # pairs of tatar words and request words
    if request.user.is_authenticated:
        for entry in History.objects.filter(user=request.user.pk):
            pairs.append((entry.tatar, entry.word))
    else:
        first_accessed = request.COOKIES.get('first_accessed')
        for key in get_redis_connection().keys(f'*h_timestamp:{first_accessed}*'):
            decoded_key = key.decode()
            timestamp_key = decoded_key[decoded_key.find(':', 1)+1:]
            pairs.append(cache.get(timestamp_key))
        pairs.sort(key=lambda i: i[2], reverse=True)  # sort by date
        pairs = list(map(lambda i: i[:-1], pairs))  # remove data info from pairs list
    return pairs
