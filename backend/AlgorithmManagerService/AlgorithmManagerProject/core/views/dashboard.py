import logging

from django.conf import settings
from django.shortcuts import render
from django.views.generic import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin

from core.models import AlgorithmModel, InputFileModel, ProcessingModel, ProcessingStatus
from django.db.models import Count


def _get_processing_count_statuses(context):
    pr_list = ProcessingModel.objects.values('status').annotate(count_processing=Count('id'))
    for item in pr_list:
        match item['status']:
            case ProcessingStatus.RUNNING:
                context['running_count'] = item['count_processing']
            case ProcessingStatus.QUEUED:
                context['queued_count'] = item['count_processing']
            case ProcessingStatus.COMPLETED:
                context['completed_count'] = item['count_processing']
            case ProcessingStatus.FAILED:
                context['failed_count'] = item['count_processing']


class DashboardView(LoginRequiredMixin, View):
    template_name = 'core/dashboard.html'

    def get(self, request):
        context = {}

        _get_processing_count_statuses(context)

        context.update({
            'algorithms_count': AlgorithmModel.objects.count(),
            'files_count': InputFileModel.objects.count(),
            'runs_count': ProcessingModel.objects.count(),
            'recent_runs': ProcessingModel.objects.select_related('algorithm', 'user')
                           .only('status', 'progress', 'user__username', 'algorithm__name', 'created_at')
                           .order_by('-created_at')[:10],
        })
        return render(request, self.template_name, context=context)
