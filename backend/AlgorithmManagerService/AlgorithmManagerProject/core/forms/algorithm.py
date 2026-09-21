from django import forms

from core.models import AlgorithmModel

CLASS_INPUT = ('block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 '
               'focus:border-blue-500 transition duration-150 ease-in-out')


class AlgorithmForm(forms.ModelForm):

    class Meta:
        model = AlgorithmModel
        fields = ['name', 'description', 'script_path', 'max_parallel_processes', 'version', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Например: VIIRS Processing', 'class': CLASS_INPUT}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Описание алгоритма', 'class': CLASS_INPUT}),
            'max_parallel_processes': forms.TextInput(attrs={'placeholder': 'Параллельные процессы', 'class': CLASS_INPUT}),
            'script_path': forms.TextInput(attrs={'placeholder': 'process_viirs_example.sh', 'class': CLASS_INPUT}),
            'version': forms.TextInput(attrs={'placeholder': '1.0.0', 'class': CLASS_INPUT}),
        }

    def clean_script_path(self):
        script_path = self.cleaned_data['script_path']
        # validate
        return script_path
