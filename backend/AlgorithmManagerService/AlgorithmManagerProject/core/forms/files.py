from urllib.parse import urlsplit

from django import forms

from core.models import InputFileModel


class InputFileForm(forms.ModelForm):

    class Meta:
        model = InputFileModel
        fields = ['filename']
        widgets = {
            'filename': forms.FileInput(attrs={'accept': '.h5'}),
        }


CLASS_INPUT = ('block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-lg focus:ring-blue-500 '
               'focus:border-blue-500 transition duration-150 ease-in-out')


class RemoteFileUploadForm(forms.Form):
    """Загрузка файлов по ссылкам (HTTP/HTTPS или FTP/FTPS), список ссылок."""

    _ALLOWED_SCHEMES = ('http', 'https', 'ftp', 'ftps')
    max_links = 50  # default

    links = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 6,
            'class': 'form-control font-mono text-sm ' + CLASS_INPUT,
            'placeholder': 'https://example.com/data.h5\nftp://ftp.example.com/incoming/data.h5',
        }),
        label='Ссылки (по одной в строке)',
    )
    ftp_username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control' + CLASS_INPUT, 'placeholder': 'anonymous (если не в ссылке)'}),
        label='FTP логин',
    )
    ftp_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control' + CLASS_INPUT, 'placeholder': 'пароль (для FTP)'}),
        label='FTP пароль',
    )

    def clean_links(self):
        raw = self.cleaned_data.get('links', '')
        lines = [ln.strip() for ln in raw.splitlines() if ln.strip()]

        if not lines:
            raise forms.ValidationError('Укажите хотя бы одну ссылку')
        if len(lines) > self.max_links:
            raise forms.ValidationError(f'Не более {self.max_links} ссылок за один раз')

        cleaned = []
        for ln in lines:
            try:
                parts = urlsplit(ln)
            except ValueError:
                raise forms.ValidationError(f'Некорректная ссылка: {ln}')
            if parts.scheme not in self._ALLOWED_SCHEMES or not parts.netloc:
                raise forms.ValidationError(
                    f'Некорректная ссылка: {ln} (допустимы http/https/ftp/ftps)'
                )
            cleaned.append(ln)
        return cleaned
