from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import JsonResponse
from django.template.loader import render_to_string
from pymorphy2 import MorphAnalyzer
from .forms import WordForm
from .utils import *


def index(request):
    """ Renders main page and handles user's word requests"""
    context = {'num_of_words': Tatar.objects.count()}
    if request.GET:
        form = WordForm(request.GET, is_authenticated=request.user.is_authenticated)
        context.update({'form': form})
        if form.is_valid():
            word, tatar_word = get_tatar_twin(form)
            context.update({'tatar_word': tatar_word})
            response = render(request, 'core/index.html', context)
            set_entry(request, tatar_word, word, response)
            return response
    else:
        form = WordForm()
        context.update({'form': form})
    return render(request, 'core/index.html', context)


def tatar_word_ajax(request):
    """ Handles ajax requests caused by submit button"""
    form = WordForm(request.GET, is_authenticated=request.user.is_authenticated)
    if form.is_valid():
        word, tatar_word = get_tatar_twin(form)
        tatar_info = render_to_string('core/tatar_info.html', {'tatar_word': tatar_word, 'word': word})
        response = JsonResponse({'status': 'OK', 'info': tatar_info})
        set_entry(request, tatar_word, word, response)
        return response
    else:
        tatar_errors = render_to_string('core/tatar_errors.html', {'form': form})
        return JsonResponse({'status': 'ERROR', 'info': tatar_errors})


def show_history(request):
    """ Renders page with history entries using paginator """
    objects_per_page = 10
    entries = get_all_entries(request)
    paginator = Paginator(entries, objects_per_page)
    page_num = request.GET.get('page', 1)
    page = paginator.get_page(page_num)
    pos_addition = (int(page_num)-1)*objects_per_page
    context = {'pairs': page.object_list, 'page': page, 'pos_addition': pos_addition}
    return render(request, 'core/history.html', context)


class TatarDetailView(DetailView):
    model = Tatar
    context_object_name = 'tatar_word'


class TopTatarListView(ListView):
    template_name = 'core/top.html'
    context_object_name = 'top_tatar_words'
    queryset = Tatar.objects.top(5)

    def get_context_data(self, *, object_list=None, **kwargs):
        parse = MorphAnalyzer().parse("раз")[0]  # To get right form of word 'раз'
        context, tatar_words_and_times_hit = super().get_context_data(), {}
        for tatar in context[self.context_object_name]:
            times = parse.make_agree_with_number(tatar.hit).word
            tatar_words_and_times_hit[tatar] = times
        context[self.context_object_name] = tatar_words_and_times_hit
        return context



