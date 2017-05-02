import os
THREATSTACK_API_KEY = os.environ.get('THREATSTACK_API_KEY')
THREATSTACK_BASE_URL = os.environ.get('THREATSTACK_BASE_URL', 'https://app.threatstack.com/api/v1')

LOGZIO_BASE_URL = os.environ.get('LOGZIO_BASE_URL',
                                 'https://listener.logz.io:8071')
LOGZIO_API_TOKEN = os.environ.get('LOGZIO_API_TOKEN')
LOGZIO_LOG_TYPE = os.environ.get('LOGZIO_LOG_TYPE', 'threatstack')

