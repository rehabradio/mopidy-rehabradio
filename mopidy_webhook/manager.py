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

    def __init__(self, config, core, player_data):
        super(QueueManager, self).__init__()
        self.core = core
        self.config = config
        self.player_data = player_data
        self.time_position = None
        self.webhook_url = config['webhook']['webhook'] + 'queues/' + \
            str(player_data['queue']) + '/head/'

    def _fetch_head_track(self, webhook_url, token):
        webhook = Webhooks(token)
        queue_track = webhook.get(self.__class__.__name__, webhook_url)

        track = queue_track['track']

        if (track['source_type'] == 'spotify'):
            queue_track['uri'] = 'spotify:track:' + track['source_id']
        elif (track['source_type'] == 'soundcloud'):
            queue_track['uri'] = 'soundcloud:song/' + track['name'] + \
                '.' + track['source_id']
        elif (track['source_type'] == 'youtube'):
            queue_track['uri'] = 'youtube:video/' + track['name'] + \
                '.' + track['source_id']
        else:
            return None
        return queue_track

    def _pop_head(self, webhook_url, token):
        webhook = Webhooks(token)
        response = webhook.delete(self.__class__.__name__, webhook_url)
        return response

    def start_track(self):
        # Grab the track at the top of the queue
        track = self._fetch_head_track(
            self.webhook_url,
            self.player_data['token']
        )
        # Add track to playlist
        self.core.tracklist.consume = True
        self.core.tracklist.add(uri=track['uri'])
        self.core.playback.next()
        # Start track
        logger.info(self.core.playback.current_track.get())
        self.time_position = track['time_position']
        self.core.playback.play()

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))

        if self.core.playback.current_track.get() is None:
            self.start_track()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def on_event(self, event, **kwargs):
        logger.info('{0} actor event: ' + event + '.'.format(
            self.__class__.__name__
        ))
        if event == 'playlists_loaded':
            pass
        if event == 'tracklist_changed':
            pass
        if event == 'track_playback_started':
            if self.time_position:
                self.core.playback.seek(self.time_position)
        if event == 'seeked':
            pass
        if event == 'track_playback_paused':
            pass
        if event == 'track_playback_resumed':
            pass
        if event == 'track_playback_ended':
            # Remove track from head of queue
            self._pop_head(
                self.webhook_url + 'pop/', self.player_data['token'])
            time.sleep(0.2)
            # Start new head track
            self.start_track()
