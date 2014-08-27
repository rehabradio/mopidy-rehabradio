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

    def get(self, class_name, webhook_url, **kwargs):
        logger.info('{0} Webhook URL: {1}'.format(class_name, webhook_url))

        try:
            response = requests.get(webhook_url, headers=self.headers)
        except Exception as e:
            logger.warning('Unable to send {0} Webhook: ({1}) {2}'.format(
                class_name,
                e.__class__.__name__,
                e.message,
            ))
        else:
            logger.info('{0} Webhook Response Status: {1}'.format(
                class_name, response.status_code
            ))
            logger.info('{0} Webhook Response Body: {1}'.format(
                class_name, response.text
            ))
        return response.json()

    def post(self, class_name, webhook_url, **kwargs):
        logger.info('{0} Webhook URL: {1}'.format(class_name, webhook_url))

        payload = json.dumps(kwargs, cls=ModelJSONEncoder, indent=2)
        logger.info('{0} Webhook Payload: {1}'.format(class_name, payload))

        try:
            response = requests.post(
                webhook_url,
                data=json.dumps(payload),
                headers=self.headers
            )
        except Exception as e:
            logger.warning('Unable to send {0} Webhook: ({1}) {2}'.format(
                class_name,
                e.__class__.__name__,
                e.message,
            ))
        else:
            logger.info('{0} Webhook Response Status: {1}'.format(
                class_name, response.status_code
            ))
            logger.info('{0} Webhook Response Body: {1}'.format(
                class_name, response.text
            ))
        return response.json()

    def put(self, class_name, webhook_url, **kwargs):
        logger.info('{0} Webhook URL: {1}'.format(class_name, webhook_url))

        payload = json.dumps(kwargs, cls=ModelJSONEncoder, indent=2)
        logger.info('{0} Webhook Payload: {1}'.format(class_name, payload))

        try:
            response = requests.put(
                webhook_url,
                data=json.dumps(payload),
                headers=self.headers
            )
        except Exception as e:
            logger.warning('Unable to send {0} Webhook: ({1}) {2}'.format(
                class_name,
                e.__class__.__name__,
                e.message,
            ))
        else:
            logger.info('{0} Webhook Response Status: {1}'.format(
                class_name, response.status_code
            ))
            logger.info('{0} Webhook Response Body: {1}'.format(
                class_name, response.text
            ))
        return response.json()

    def patch(self, class_name, webhook_url, **kwargs):
        logger.info('{0} Webhook URL: {1}'.format(class_name, webhook_url))

        payload = json.dumps(kwargs, cls=ModelJSONEncoder, indent=2)
        logger.info('{0} Webhook Payload: {1}'.format(class_name, payload))

        try:
            response = requests.patch(
                webhook_url,
                data=json.dumps(payload),
                headers=self.headers
            )
        except Exception as e:
            logger.warning('Unable to send {0} Webhook: ({1}) {2}'.format(
                class_name,
                e.__class__.__name__,
                e.message,
            ))
        else:
            logger.info('{0} Webhook Response Status: {1}'.format(
                class_name, response.status_code
            ))
            logger.info('{0} Webhook Response Body: {1}'.format(
                class_name, response.text
            ))
        return response.json()

    def delete(self, class_name, webhook_url, **kwargs):
        logger.info('{0} Webhook URL: {1}'.format(class_name, webhook_url))

        payload = json.dumps(kwargs, cls=ModelJSONEncoder, indent=2)
        logger.info('{0} Webhook Payload: {1}'.format(class_name, payload))

        try:
            response = requests.delete(webhook_url, headers=self.headers)
        except Exception as e:
            logger.warning('Unable to send {0} Webhook: ({1}) {2}'.format(
                class_name,
                e.__class__.__name__,
                e.message,
            ))
        else:
            logger.info('{0} Webhook Response Status: {1}'.format(
                class_name, response.status_code
            ))
            logger.info('{0} Webhook Response Body: {1}'.format(
                class_name, response.text
            ))
        return response.json()
