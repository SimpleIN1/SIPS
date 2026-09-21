from django import forms

from core.models import ProcessingModel, AlgorithmModel, InputFileModel


class ProcessingForm(forms.ModelForm):
    """Форма для запуска алгоритма."""

    class Meta:
        model = ProcessingModel
        fields = ['algorithm', 'output_path', 'use_sudo']
        widgets = {
            'algorithm': forms.Select(attrs={'class': 'form-select algorithm-select py-2 px-2'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только активные алгоритмы
        self.fields['algorithm'].queryset = AlgorithmModel.objects.filter(is_active=True)
