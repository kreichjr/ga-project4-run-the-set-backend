"""
WSGI config for run_the_set_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/my-project-dir')  # adjust as appropriate
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'run_the_set_backend.settings')

application = get_wsgi_application()
