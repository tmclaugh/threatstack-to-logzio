'''
Send alert events to Logz.io.
'''

from flask import Blueprint, jsonify, request
import logging
import app.models.logzio as logzio_model
import app.models.threatstack as threatstack_model
from app.sns import check_aws_sns

_logger = logging.getLogger(__name__)

logzio = Blueprint('logzio', __name__)

#decerator refers to the blueprint object.
@logzio.route('/status', methods=['GET'])
def is_available():
    '''
    Test that Threat Stack and Logz.io are reachable.
    '''
    _logger.info('{}: {}'.format(request.method, request.path))

    lgz = logzio_model.LogzioModel()
    logzio_status = lgz.is_available()
    logzio_info = {'success': logzio_status}

    ts = threatstack_model.ThreatStackModel()
    ts_status = ts.is_available()
    ts_info = {'success': ts_status}

    status_code = 200
    if logzio_status and ts_status:
        success = True
    else:
        success = False

    return jsonify(success=success, logzio=logzio_info, threatstack=ts_info), status_code

@logzio.route('/alert', methods=['POST'])
@check_aws_sns
def put_alert():
    '''
    Send Threat Stack alerts to Logz.io.
    '''
    _logger.info('{}: {} - {}'.format(request.method,
                                      request.path,
                                      request.data))

    webhook_data = request.get_json(force=True)
    for alert in webhook_data.get('alerts'):
        ts = threatstack_model.ThreatStackModel()
        alert_full = ts.get_alert_by_id(alert.get('id'))
        lgz = logzio_model.LogzioModel()
        logzio_resp = lgz.put_alert_event(alert_full)

    status_code = 200
    success = True
    response = {'success': success, 'logzio': logzio_resp}

    return jsonify(response), status_code

