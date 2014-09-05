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


class QueueManager(pykka.ThreadingActor, CoreListener):
    """Manages the tracklist and playback for the mopidy server,
    based on the current head track.
    """
    def __init__(self, config, core, player_data):
        super(QueueManager, self).__init__()
        self.core = core
        self.webhook = Webhooks(config['webhook']['token'])
        self.webhook_url = config['webhook']['webhook'] + 'queues/' + \
            str(player_data['queue']['id']) + '/head/'

    def _fetch_head_track(self, webhook_url):
        logger.info('Fetching head track')
        return self.webhook.get(self.__class__.__name__, webhook_url)

    def _start_track(self):
        logger.info('Playing Track')
        self.core.tracklist.clear()
        track = self._fetch_head_track(self.webhook_url)
        # Add track to queue
        self.core.tracklist.add(uri=track['track']['uri'])
        # Set track to active
        self.core.playback.play()

        if track['time_position']:
            self.core.playback.pause()
            self._seek_track(track)

    def _next_track(self):
        logger.info('Removing head track')
        self.webhook.delete(self.__class__.__name__, self.webhook_url + 'pop/')
        time.sleep(1)
        self._start_track()

    def _seek_track(self, track):
        seek_time = track['time_position'] + 2000
        if seek_time >= track['track']['duration_ms']:
            self._next_track()
        else:
            time.sleep(2)
            self.core.playback.seek(track['time_position'])

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        # Play a track once, then remove from queue
        self.core.tracklist.consume = True
        self._start_track()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))
        # Empty queue
        self.core.tracklist.clear()

    def on_event(self, event, **kwargs):
        if event == 'track_playback_ended':
            # Start new head track
            self._next_track()
