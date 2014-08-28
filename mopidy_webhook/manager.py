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
        self.config = config
        self.player_data = player_data
        self.time_position = None
        self.webhook = Webhooks(config['webhook']['token'])
        self.webhook_url = config['webhook']['webhook'] + 'queues/' + \
            str(player_data['queue']['id']) + '/head/'

    def _fetch_head_track(self, webhook_url):
        logger.info('Fetching head track')
        queue_track = self.webhook.get(self.__class__.__name__, webhook_url)

        track = queue_track['track']

        if (track['source_type'] == 'spotify'):
            queue_track['uri'] = 'spotify:track:' + track['source_id']
        elif (track['source_type'] == 'soundcloud'):
            queue_track['uri'] = 'soundcloud:song/' + track['name'] + \
                '.' + track['source_id']
        else:
            return None
        return queue_track

    def _pop_head(self, webhook_url):
        logger.info('Removing head track')
        self.webhook.delete(self.__class__.__name__, webhook_url)

    def _start_track(self):
        # Grab the track at the top of the queue
        track = self._fetch_head_track(self.webhook_url)
        # Set the start position of the track
        self.time_position = track['time_position']
        # Add track to playlist
        self.core.tracklist.add(uri=track['uri'])
        self.core.playback.next()
        # Play track
        logger.info('Now playling {0}'.format(
            self.core.playback.current_track.get()))
        self.core.playback.play()
        if self.time_position:
            self.core.playback.pause()

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
        if event == 'track_playback_started' and self.time_position:
            # Resumse the track, from last recorded time postion on the server
            logger.info('{0} actor seeked.'.format(self.__class__.__name__))
            self.core.playback.seek(self.time_position)
        if event == 'track_playback_ended':
            # Remove track from head of queue
            self._pop_head(self.webhook_url + 'pop/')
            time.sleep(0.2)
            # Start new head track
            self._start_track()
