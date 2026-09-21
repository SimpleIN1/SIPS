from django.db.models import Count
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView, DetailView

from core.forms.algorithm import AlgorithmForm
from core.models import AlgorithmModel


class AlgorithmListView(LoginRequiredMixin, ListView):
    template_name = 'core/algorithms_list.html'
    queryset = AlgorithmModel.objects.annotate(processing_count=Count('processing')).order_by('-created_at')
    context_object_name = 'algorithms'


class AlgorithmCreateView(LoginRequiredMixin, CreateView):
    template_name = 'core/algorithm_form.html'
    form_class = AlgorithmForm
    success_url = reverse_lazy("core:algorithms_list")

    def form_valid(self, form):
        messages.success(self.request, 'Алгоритм создан')
        return super().form_valid(form)


class AlgorithmUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'core/algorithm_form.html'
    form_class = AlgorithmForm
    model = AlgorithmModel
    success_url = reverse_lazy("core:algorithms_list")

    def form_valid(self, form):
        messages.success(self.request, 'Алгоритм обновлён')
        return super().form_valid(form)
