# future imports
from __future__ import unicode_literals

# stdlib imports
import logging

# third-party imports
import pykka
from mopidy.core import CoreListener

# local imports
from playback import WebhookPlayback
from reporters import EventReporter, StatusReporter
from session import WebhookSession


logger = logging.getLogger(__name__)


class WebhookFrontend(pykka.ThreadingActor, CoreListener):
    def __init__(self, config, core):
        super(WebhookFrontend, self).__init__()
        self.config = config
        self.core = core
        self.start_reporters = False
        self.event_reporter = None
        self.playback = None
        self.session = WebhookSession(config)
        self.status_reporter = None

    def on_start(self):
        self.session.start()

        self.playback = WebhookPlayback.start(
            self.config, self.core, self.session)

        self.event_reporter = EventReporter.start(
            self.config, self.core, self.session)
        self.status_reporter = StatusReporter.start(
            self.config, self.core, self.session)

    def on_event(self, event, **kwargs):
        pass

    def _stop_children(self):
        self.event_reporter.stop()
        self.playback.stop()
        self.status_reporter.stop()

    def on_stop(self):
        self.session.stop()
        self._stop_children()

    def on_failure(self, exception_type, exception_value, traceback):
        self._stop_children()
