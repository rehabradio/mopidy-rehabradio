# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging

# third-party imports
import requests
from mopidy.models import ModelJSONEncoder


logger = logging.getLogger(__name__)


class Webhooks(object):

    def __init__(self, token):
        self.headers = {
            'PLAYER_AUTH_TOKEN': token,
            'content-type': 'application/json'
        }

    def _send_request(self, webhook, webhook_url, data=None):
        payload = {}
        response_data = {}

        if data:
            payload = json.dumps(data, cls=ModelJSONEncoder, indent=2)
        try:
            response = webhook(webhook_url, headers=self.headers, data=json.dumps(payload))
        except Exception as e:
            logger.warning('Unable to send Webhook: ({0}) {1}'.format(
                e.__class__.__name__,
                e.message,
            ))
        else:
            if response.status_code != 200:
                logger.warning(
                    'Bad status code returned: ({0}) {1}: {2}'.format(
                        response.status_code,
                        response.request.method,
                        webhook_url,
                    )
                )

            try:
                response_data = response.json()
            except Exception as e:
                logger.warning(
                    'Invalid response returned: ({0}) {1}'.format(
                        e.__class__.__name__,
                        e.message,
                    )
                )

        return response_data

    def get(self, webhook_url, **kwargs):
        webhook = requests.get
        return self._send_request(webhook, webhook_url)

    def post(self, webhook_url, **kwargs):
        webhook = requests.post
        return self._send_request(webhook, webhook_url, kwargs)

    def put(self, webhook_url, **kwargs):
        webhook = requests.put
        return self._send_request(webhook, webhook_url, kwargs)

    def patch(self, webhook_url, **kwargs):
        webhook = requests.patch
        return self._send_request(webhook, webhook_url, kwargs)

    def delete(self, webhook_url, **kwargs):
        webhook = requests.delete
        return self._send_request(webhook, webhook_url, kwargs)
