import sys
import logging

logging.basicConfig(level=logging.DEBUG, filename='/var/www/html/garden-automation/garden_automation.log',
					format='%(asctime)s %(message)s')
sys.path.insert(0, '/var/www/html/garden-automation')
sys.path.insert(0, '/var/www/html/garden-automation/.venv/lib/python3.9/site-packages')
from app import app as application
