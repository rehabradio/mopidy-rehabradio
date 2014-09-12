# future imports
from __future__ import unicode_literals

# stdlib imports
import logging
import time
import threading

# third-party imports
import pykka
from mopidy.core import CoreListener


logger = logging.getLogger(__name__)


class WebhookPlayback(pykka.ThreadingActor, CoreListener):
    """Control the tracklist and playback functionality of mopidy.
    Fetches the head track, adds to tracklist, and starts playback.
    If a timelapse is set, then the track is seeked to the given position.

    Note that it also sends status reports every 2 seconds while
    a track is playing to update the server information to sync the track.
    """

    def __init__(self, config, core, session):
        super(WebhookPlayback, self).__init__()
        self.config = config
        self.core = core
        self.session = session
        self.timer = None

    def on_start(self):
        # Wait a couple of seconds, to let mopidy settle
        time.sleep(4)
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        # Set track to play a track once, then remove from tracklist
        self.core.tracklist.consume = True
        self._start_head_track()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))
        # Empty queue
        self.core.tracklist.clear()
        self.timer.cancel()

    def on_event(self, event, **kwargs):
        if event == 'track_playback_started':
            self.update_status()
        elif event == 'track_playback_ended':
            self.timer.cancel()
            self._next_head_track()

    def update_status(self):
        time.sleep(1)
        if self.core.playback.current_track.get():
            kwargs = {
                'state': self.core.playback.state.get(),
                'time_position': self.core.playback.time_position.get(),
            }
            self.session.update_head(kwargs)

        self.timer = threading.Timer(1, self.update_status)
        self.timer.start()

    def _next_head_track(self):
        # Start new head track
        self.session.pop_head()
        # Allow some time for the api server to update
        time.sleep(0.5)
        self._start_head_track()

    def _seek_track(self, track):
        seek_time = track['time_position'] + 1500
        if seek_time >= track['track']['duration_ms']:
            self._next_head_track()
        else:
            time.sleep(1.5)
            self.core.playback.seek(track['time_position'])

    def _start_head_track(self):
        # then fetch the head track
        self.core.tracklist.clear()
        track = self.session.fetch_head()
        # Add track to queue
        self.core.tracklist.add(uri=track['track']['uri'])
        # Set track to active
        self.core.playback.play()

        if track['time_position']:
            self.core.playback.pause()
            self._seek_track(track)
