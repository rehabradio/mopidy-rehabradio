# future imports
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka
from mopidy.core import CoreListener

# local imports
from webhooks import Webhooks
from reporters import EventReporter, StatusReporter
from manager import QueueManager


logger = logging.getLogger(__name__)


def _fetch_player_data(class_name, config):
    token = config['webhook']['token']
    webhook = Webhooks(token)
    webhook_url = config['webhook']['webhook'] + 'players/' + token + '/'
    response = webhook.get(class_name, webhook_url)

    return response


class WebhookFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(WebhookFrontend, self).__init__()
        self.config = config
        self.core = core
        self.event_reporter = None
        self.status_reporter = None
        self.player_data = _fetch_player_data(self.__class__.__name__, config)

    def on_start(self):
        # Updates the queued track based on events triggered by mopidy
        self.event_reporter = EventReporter.start(
            self.config, self.core, self.player_data)
        # Updates the queued track based on status updates triggered by mopidy
        self.status_reporter = StatusReporter.start(
            self.config, self.core, self.player_data)
        # Tracklist and playback management
        self.track_reporter = QueueManager.start(
            self.config, self.core, self.player_data)

    def _stop_children(self):
        self.event_reporter.stop()
        self.status_reporter.stop()
        self.track_reporter.stop()

    def on_stop(self):
        self._stop_children()

    def on_failure(self, exception_type, exception_value, traceback):
        self._stop_children()
