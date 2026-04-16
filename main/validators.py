from django.core.exceptions import ValidationError
from django.conf import settings

def validate_file_size(value):
    if value.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(f"The maximum file size is {settings.FILE_UPLOAD_MAX_MEMORY_SIZE/1024**2} MB.")
    return value
  