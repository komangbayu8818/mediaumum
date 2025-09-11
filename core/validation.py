from django.core.exceptions import ValidationError

def validate_judul(value):
    if len(value) < 10:
        raise ValidationError('judul kurang dari 10 karakter')