"""
Models and managers for storing and processing info about tatar words and results of users' requests

Main models are following:

    1. Tatar - Tatar word
    2. Translations - Translation of the particular tatar word
    3. Examples - Translation usage examples

"""

from django.db import models
from django.conf import settings
from django.db.models import F


class TatarManager(models.Manager):
    # Long query string for fetching similar tatar word, referred here as a 'twin'
    TWIN_QUERY_STRING = """
                   SELECT *, word <-> %s AS dist
                   FROM (
  	                    SELECT *
	                    FROM core_tatar
	                    WHERE levenshtein(word, %s) = (
		                    SELECT min(levenshtein(word, %s))
                            FROM core_tatar)
                        ) AS _
                    ORDER BY dist, word
                    LIMIT 1
                   """

    def find_twin(self, word):
        """
        Finds twin using TWIN_QUERY_STRING

        Examples:
            "Папа" -> "Папас"
            "Щука" -> "Ука"
            "Автомобиль" -> "Автомобиль"
            "опаврполыорлпулопыптывалмтлыиплоыипжлпеиплдыокпидл" -> "Борылмалы-сыгылмалы итеп"
        """
        tatar_word = self.raw(self.TWIN_QUERY_STRING, [word]*3)[0]
        return tatar_word

    def top(self, number):
        """Fetches N words with the highest 'hit' parameter"""
        return self.order_by('-hit')[:number]


class HistoryManager(models.Manager):
    MAX_PER_USER = 100  # Max amount of history entries for user

    def create(self, user, tatar_word, word):
        """
        If number of history entries reached MAX_PER_USER,
        delete the oldest entry before adding the new one
        """
        if user.entries.count() == self.MAX_PER_USER:
            user.entries.last().delete()
        super().create(user=user, tatar=tatar_word, word=word)


class CommentManager(models.Manager):
    MAX_PER_WORD = 10

    def create(self, user, word, comment):
        if word.comments.count() == self.MAX_PER_WORD:
            word.comments.first().delete()
        super().create(user=user, word=word, comment=comment)


class Tatar(models.Model):
    # Actual word
    word = models.TextField(unique=True, verbose_name="Татарское слово")
    # Times the word was fetched on users' request
    hit = models.BigIntegerField(default=0, verbose_name="Кол-во подборов")

    objects = TatarManager()

    class Meta:
        verbose_name = 'Слово на татарском'
        verbose_name_plural = 'Слова на татарском'
        ordering = ['word']

    def __str__(self):
        return self.word

    def hit_increment(self):
        """When fetched, incr the 'hit' parameter"""
        self.hit = F('hit') + 1
        self.save()


class Translation(models.Model):
    # Tatar word to which translation is related
    tatar = models.ForeignKey(Tatar, models.CASCADE, blank=True,
                              null=True, related_name='translations',
                              verbose_name='Татарское слово')
    # Actual translation
    translation = models.TextField(blank=True, null=True, verbose_name="Перевод")

    class Meta:
        verbose_name = 'Перевод'
        verbose_name_plural = 'Переводы'
        ordering = ['translation']

    def __str__(self):
        return self.translation


class Example(models.Model):
    # Translation to which example is related
    trans = models.ForeignKey(Translation, models.CASCADE, blank=True,
                              null=True, related_name='examples',
                              verbose_name='Пример')
    # Actual example
    example = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Пример'
        verbose_name_plural = 'Примеры'
        ordering = ['example']

    def __str__(self):
        return self.example


class History(models.Model):
    """for storing authorized users' results of inputs"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Юзер', related_name='entries')
    tatar = models.ForeignKey(Tatar, on_delete=models.CASCADE,
                              verbose_name='Татарское слово', related_name='entries')
    word = models.TextField(verbose_name="Введенное слово")
    hit_timestamp = models.DateTimeField(auto_now_add=True,
                                         verbose_name='Введено')

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'История'
        ordering = ['-hit_timestamp']

    objects = HistoryManager()

    def __str__(self):
        return f'{self.word}: {self.hit_timestamp}'


class Comment(models.Model):
    """for storing users' comments"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Юзер', related_name='comments')
    comment = models.TextField(verbose_name='Комментарий')
    word = models.ForeignKey(Tatar, on_delete=models.CASCADE,
                             verbose_name='Слово', related_name='comments')
    sent_timestamp = models.DateTimeField(auto_now_add=True,
                                          verbose_name='Оставлено')

    class Meta:
        verbose_name = 'История'
        verbose_name_plural = 'История'
        ordering = ['sent_timestamp']

    objects = CommentManager()

    def __str__(self):
        return f'{self.comment}: {self.sent_timestamp}'



