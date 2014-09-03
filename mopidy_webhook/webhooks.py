# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging

# third-party imports
import requests
from mopidy.models import ModelJSONEncoder

# local imports
from utils.exceptions import BadRequest


logger = logging.getLogger(__name__)


class Webhooks(object):

    def __init__(self, token):
        self.headers = {
            'PLAYER_AUTH_TOKEN': token,
            'content-type': 'application/json'
        }

    def _send_request(self, webhook, class_name, webhook_url, data=None):

        logger.info('{0} Webhook URL: {1}'.format(class_name, webhook_url))

        payload = {}
        if data:
            payload = json.dumps(data, cls=ModelJSONEncoder, indent=2)
            logger.info('{0} Webhook Payload: {1}'.format(class_name, payload))

        try:
            response = webhook(
                webhook_url, headers=self.headers, data=json.dumps(payload))
        except Exception as e:
            logger.warning('Unable to send {0} Webhook: ({1}) {2}'.format(
                class_name,
                e.__class__.__name__,
                e.message,
            ))
            raise BadRequest('Unable to send {0} Webhook: ({1}) {2}'.format(
                class_name,
                e.__class__.__name__,
                e.message,
            ))
        else:
            if response.status_code != 200:
                raise BadRequest('{0} Bad status code returned: ({1}) {2}'.format(
                    class_name,
                    response.status_code,
                    webhook_url
                ))

            try:
                response_data = response.json()
            except Exception as e:
                raise BadRequest('{0} Invalid response returned: ({1}) {2}'.format(
                    class_name,
                    e.__class__.__name__,
                    e.message,
                ))

            logger.info('{0} Webhook Response Status: {1}'.format(
                class_name, response.status_code
            ))
            logger.info('{0} Webhook Response Body: {1}'.format(
                class_name, response_data
            ))

        return response_data

    def get(self, class_name, webhook_url, **kwargs):
        webhook = requests.get
        return self._send_request(webhook, class_name, webhook_url)

    def post(self, class_name, webhook_url, **kwargs):
        webhook = requests.post
        return self._send_request(webhook, class_name, webhook_url, kwargs)

    def put(self, class_name, webhook_url, **kwargs):
        webhook = requests.put
        return self._send_request(webhook, class_name, webhook_url, kwargs)

    def patch(self, class_name, webhook_url, **kwargs):
        webhook = requests.patch
        return self._send_request(webhook, class_name, webhook_url, kwargs)

    def delete(self, class_name, webhook_url, **kwargs):
        webhook = requests.delete
        return self._send_request(webhook, class_name, webhook_url)
