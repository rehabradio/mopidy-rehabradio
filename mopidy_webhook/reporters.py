# future imports
from __future__ import unicode_literals

# stdlib imports
import logging
import time

# third-party imports
import pykka
from mopidy.core import CoreListener


logger = logging.getLogger(__name__)


class StatusReporter(pykka.ThreadingActor):

    def __init__(self, config, core, session):
        super(StatusReporter, self).__init__()
        self.base_url = config['webhook']['webhook']
        self.config = config
        self.core = core
        self.in_future = self.actor_ref.proxy()
        self.session = session

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        self.report_status()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def report_status(self):
        kwargs = {
            'current_track': self.core.playback.current_track.get(),
            'state': self.core.playback.state.get(),
            'time_position': self.core.playback.time_position.get(),
        }
        #self.session.report_status(**kwargs)
        time.sleep(2)
        self.in_future.report_status()


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, config, core, session):
        super(EventReporter, self).__init__()
        self.base_url = config['webhook']['webhook']
        self.config = config
        self.session = session

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def on_event(self, event, **kwargs):
        #self.session.report_event(**kwargs)
        pass
