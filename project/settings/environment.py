from pathlib import Path
from utils.environment import parse_comaa_sep_str_to_list, get_env_variable
import os

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE') # noqa E501
DEBUG = True if os.environ.get('DEBUG') == '1' else False

ALLOWED_HOSTS: list[str] = parse_comaa_sep_str_to_list(get_env_variable('ALLOWED_HOSTS')) # noqa E501
CSRF_TRUSTED_ORIGINS: list[str] = parse_comaa_sep_str_to_list(get_env_variable('CSRF_TRUSTED_ORIGINS')) # noqa E501

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination', # noqa E501
    'PAGE_SIZE': 10,
}
