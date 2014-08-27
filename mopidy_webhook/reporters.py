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
    """Updates the API server with tracklist and playback status.
    """
    def __init__(self, config, core, player_data):
        super(StatusReporter, self).__init__()
        self.config = config
        self.core = core
        self.player_data = player_data
        self.in_future = self.actor_ref.proxy()
        self.webhook = Webhooks(config['webhook']['token'])

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        self.report_status()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

        webhook_url = self.config['webhook']['webhook'] + 'queues/' + \
            str(self.player_data['queue']) + '/head/status/'
        kwargs = {
            'current_track': self.core.playback.current_track.get(),
            'state': 'stopped',
            'time_position': self.core.playback.time_position.get(),
        }

        self.webhook.post(self.__class__.__name__, webhook_url, **kwargs)

    def report_status(self):
        webhook_url = self.config['webhook']['webhook'] + 'queues/' + \
            str(self.player_data['queue']) + '/head/status/'
        kwargs = {
            'current_track': self.core.playback.current_track.get(),
            'state': self.core.playback.state.get(),
            'time_position': self.core.playback.time_position.get(),
        }

        self.webhook.post(self.__class__.__name__, webhook_url, **kwargs)

        # Loop back on itself every 2 seconds
        time.sleep(2)
        self.in_future.report_status()


class EventReporter(pykka.ThreadingActor, CoreListener):
    """Updates the API server each time an event is trigered by mopidy.
    """
    def __init__(self, config, core, player_data):
        super(EventReporter, self).__init__()
        self.core = core
        self.config = config
        self.player_data = player_data
        self.time_position = None
        self.webhook = Webhooks(config['webhook']['token'])

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def on_event(self, event, **kwargs):
        logger.info('{0} actor event: {1}.'.format(
            self.__class__.__name__, event))

        webhook_url = '{0}queues/{1}/head/events/{2}/'.format(
            self.config['webhook']['webhook'],
            self.player_data['queue'],
            event
        )

        self.webhook.post(self.__class__.__name__, webhook_url, **kwargs)
