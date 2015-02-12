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
        self.core.tracklist.consume = True
        self.session = session
        self.track = self.session.fetch_head()
        self.timer = None

    def on_start(self):
        """Add the track to the tracklist, then play.
        If the track has a time position, then pause and seek the track to the given time.
        """
        self.core.tracklist.add(uri=self.track['track']['uri'])
        self.core.playback.play()

        if self.track['time_position']:
            self.core.playback.pause()
            self._seek_track()

        # Start update task
        self.update_status()

    def on_stop(self):
        # Empty queue
        self.core.tracklist.clear()
        if self.timer:
            self.timer.cancel()

    def update_status(self):
        if self.core.playback.current_track.get():
            kwargs = {
                'state': self.core.playback.state.get(),
                'time_position': self.core.playback.time_position.get(),
            }
            self.session.update_head(kwargs)

        time_til_end = self.track['track']['duration_ms'] - self.core.playback.time_position.get()

        # If there is less than 8 seconds left on the track, add the next track
        if time_til_end < 8000 and self.core.tracklist.length.get() < 2:
            self.session.pop_head()
            self.track = self.session.fetch_head()
            self.core.tracklist.add(uri=self.track['track']['uri'])

            if self.core.playback.state.get() != 'playing':
                self.core.playback.play()

        self.timer = threading.Timer(3, self.update_status)
        self.timer.start()

    def _seek_track(self):
        seek_time = self.track['time_position'] + 1500
        if seek_time >= self.track['track']['duration_ms']:
            self._next_head_track()
        else:
            time.sleep(1.5)
            self.core.playback.seek(seek_time)
