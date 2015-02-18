# future imports
from __future__ import unicode_literals

# stdlib imports
import logging

# local imports
from webhooks import Webhooks


logger = logging.getLogger(__name__)


class WebhookSession(object):

    def __init__(self, config):
        self.webhook = Webhooks(config['webhook']['token'])
        self.base_url = config['webhook']['webhook']

    def start(self):
        logger.info('Session started.')

    def stop(self):
        logger.info('Session ended.')

    def fetch_head(self):
        logger.info('Fetching head track.')
        webhook_url = '{0}queues/head/'.format(self.base_url)

        return self.webhook.get(webhook_url)

    def pop_head(self, kwargs):
        logger.info('Removing current head track.')
        webhook_url = '{0}queues/head/'.format(self.base_url)

        return self.webhook.delete(webhook_url, **kwargs)

    def update_head(self, kwargs):
        logger.info('Updating current head track.')
        webhook_url = '{0}queues/head/'.format(self.base_url)

        return self.webhook.patch(webhook_url, **kwargs)
