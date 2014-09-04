# future imports
from __future__ import unicode_literals

# stdlib imports
import logging
import time
import Queue

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

    def _pop_head(self, webhook_url):
        logger.info('Removing head track')
        self.webhook.delete(self.__class__.__name__, webhook_url)

    def _start_track(self):
        track = self._fetch_head_track(self.webhook_url)
        q = Queue.Queue()
        # Add track to queue
        q.put(lambda: self.core.tracklist.add(uri=track['track']['uri']))
        # Set track to active
        q.put(lambda: self.core.playback.play())
        q.put(lambda: self.core.playback.pause())
        q.put(lambda: self.core.playback.seek(track['time_position']))

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        self.core.tracklist.clear()
        # Play a track once, then remove from queue
        self.core.tracklist.consume = True
        self._start_track()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))
        # Empty queue
        self.core.tracklist.clear()

    def on_event(self, event, **kwargs):
        if event == 'track_playback_ended':
            q = Queue.Queue()
            # Remove track from head of queue
            q.put(lambda: self._pop_head(self.webhook_url + 'pop/'))
            # Start new head track
            q.put(lambda: self._start_track())
            while not q.empty():
                func = q.get()
                time.sleep(0.1)
                func()
