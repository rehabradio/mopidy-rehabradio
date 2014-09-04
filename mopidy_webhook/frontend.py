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
from reporters import EventReporter, StatusReporter
from manager import QueueManager


logger = logging.getLogger(__name__)


class WebhookFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(WebhookFrontend, self).__init__()
        self.config = config
        self.core = core
        self.start_reporters = False

    def _fetch_player_data(self):
        token = self.config['webhook']['token']
        webhook = Webhooks(token)
        webhook_url = self.config['webhook']['webhook'] + 'players/' + token + '/'

        return webhook.get(self.__class__.__name__, webhook_url)

    def on_start(self):
        self.player_data = self._fetch_player_data()
        # Tracklist and playback management
        self.queue_manager = QueueManager.start(
            self.config, self.core, self.player_data)

    def on_event(self, event, **kwargs):
        # Wait until track is loaded and seeked to start reporters
        if event == 'seeked' and self.start_reporters is False:
            self.start_reporters = True
            # Updates the queued track based on status updates
            self.status_reporter = StatusReporter.start(
                self.config, self.core, self.player_data)
            # Updates the queued track based on events triggered by mopidy
            self.event_reporter = EventReporter.start(
                self.config, self.core, self.player_data)

    def _stop_children(self):
        self.event_reporter.stop()
        self.status_reporter.stop()
        self.queue_manager.stop()

    def on_stop(self):
        self._stop_children()

    def on_failure(self, exception_type, exception_value, traceback):
        self._stop_children()
