'''Logz.io model'''

from app.errors import AppBaseError
import config
import logging
import requests
import six
import sys

_logger = logging.getLogger(__name__)

LOGZIO_API_TOKEN = config.LOGZIO_API_TOKEN
LOGZIO_LOG_TYPE = config.LOGZIO_LOG_TYPE
LOGZIO_BASE_URL = config.LOGZIO_BASE_URL

class LogzioBaseError(AppBaseError):
    '''Base Logz.io Exception class'''

class LogzioRequestError(LogzioBaseError):
    '''Logz.io request error'''

class LogzioAPIError(LogzioBaseError):
    '''Logz.io API error'''

class LogzioModel(object):
    def __init__(self,
                logzio_base_url=LOGZIO_BASE_URL,
                logzio_token=LOGZIO_API_TOKEN,
                logzio_log_type=LOGZIO_LOG_TYPE):

        self.logzio_base_url = logzio_base_url
        self.logzio_token = logzio_token
        self.logzio_log_type = logzio_log_type

    def _make_logzio_request(self, request_type, json_data=None):
        '''Make requests to Logz.io'''
        url = '{}/?token={}&type={}'.format(self.logzio_base_url,
                                            self.logzio_token,
                                            self.logzio_log_type)
        _logger.debug(url)
        try:
            resp = requests.request(
                request_type,
                url,
                json=json_data
            )

        except requests.exceptions.RequestException as e:
            exc_info = sys.exc_info()
            if sys.version_info >= (3,0,0):
                raise LogzioRequestError(e).with_traceback(exc_info[2])
            else:
                six.reraise(
                    LogzioRequestError,
                    LogzioRequestError(e),
                    exc_info[2]
                )

        if not resp.ok:
            if 'application/json' in resp.headers.get('Content-Type'):
                raise LogzioAPIError(
                    resp.reason,
                    resp.status_code,
                    resp.json()
                )
            else:
                raise LogzioRequestError(resp.reason, resp.status_code)

        return True


    def is_available(self):
        '''Check if Logz.io is available'''
        # This is enough to check connection and token validity

        return self._make_logzio_request('POST')

    def put_alert_event(self, alert):
        '''Send an alert to Logzio'''

        if self._make_logzio_request('POST', alert):
            r = {'success': True}
        else:
            r = {'success': False}

        return r

