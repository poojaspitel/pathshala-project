import os
import sys
import django
import io

# Ensure parent folder (project root) is on sys.path so `web` package is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
from django.core.management import call_command

s = io.StringIO()
call_command('dumpdata', '--natural-primary', '--natural-foreign', '--indent', '2', stdout=s)
with open('alldata.json', 'w', encoding='utf-8') as f:
    f.write(s.getvalue())
print('wrote alldata.json (utf-8)')
