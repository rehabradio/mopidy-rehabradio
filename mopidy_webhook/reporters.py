# future imports
from __future__ import unicode_literals

# stdlib imports
import logging
import time

# third-party imports
import pykka
from mopidy.core import CoreListener

# local imports
from webhooks import Webhooks


logger = logging.getLogger(__name__)


class StatusReporter(pykka.ThreadingActor):

    def __init__(self, config, core, player_data):
        super(StatusReporter, self).__init__()
        self.config = config
        self.core = core
        self.player_data = player_data
        self.in_future = self.actor_ref.proxy()

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        self.report_status()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))
        token = self.config['webhook']['token']
        webhook = Webhooks(token)
        webhook_url = self.config['webhook']['webhook'] + 'queues/' + \
            str(self.player_data['queue']) + '/head/status/'
        kwargs = {
            'current_track': self.core.playback.current_track.get(),
            'state': "stopped",
            'time_position': self.core.playback.time_position.get(),
        }
        webhook.post(self.__class__.__name__, webhook_url, **kwargs)

    def report_status(self):
        token = self.config['webhook']['token']
        webhook = Webhooks(token)
        webhook_url = self.config['webhook']['webhook'] + 'queues/' + \
            str(self.player_data['queue']) + '/head/status/'
        kwargs = {
            'state': self.core.playback.state.get(),
        }
        webhook.post(self.__class__.__name__, webhook_url, **kwargs)
        time.sleep(2)
        self.in_future.report_status()


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, config, core, player_data):
        super(EventReporter, self).__init__()
        self.config = config
        self.player_data = player_data

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        pass

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))
        pass

    def on_event(self, event, **kwargs):
        token = self.config['webhook']['token']
        webhook = Webhooks(token)
        webhook_url = self.config['webhook']['webhook'] + 'players/' + \
            token + '/event/' + event + '/'
        kwargs = {
            'event': event,
        }
        webhook.post(self.__class__.__name__, webhook_url, **kwargs)
