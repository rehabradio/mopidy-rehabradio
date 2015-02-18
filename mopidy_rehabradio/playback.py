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

    track = None
    queue = None
    playback_timer = None
    track_timer = None
    update_timer = None
    stop_timer = False

    def __init__(self, config, core, session):
        super(WebhookPlayback, self).__init__()
        self.config = config
        self.core = core
        self.core.tracklist.consume = True
        self.session = session

    def on_start(self):
        """Add the track to the tracklist, then play.
        If the track has a time position, then pause
        and seek the track to the given time.
        """
        self.track = self.session.fetch_head()
        if self.track['track']:
            self.queue = self.track['queue']
            self._start()
        else:
            self.playback_timer = threading.Timer(1, self.on_start)
            self.playback_timer.start()

    def _start(self):
        """Start the loaded track, and start sending updates to the server.
        """
        # Start track
        self._play_track()
        # Start tracking the song
        self.track_song()
        # Start update task
        self.update_status()

    def on_stop(self):
        """Update the server to show the track has finished.
        Also clears all the tracks from the tracklist
        and cancels any running threads.
        """
        # Stop any new timers
        self.stop_timer = True

        if self.track.get('track') and self.track['track']:
            kwargs = {
                'queue_id': self.queue,
                'state': 'stopped',
            }
            self.session.update_head(kwargs)

        # Empty queue
        self.core.tracklist.clear()

        # Stop repeating tasks (update/playback)
        if self.update_timer:
            self.update_timer.cancel()
        if self.track_timer:
            self.track_timer.cancel()
        if self.playback_timer:
            self.playback_timer.cancel()

    def on_event(self, event):
        if event == 'tracklist_changed':
            if self.core.playback.time_position.get() == 0:
                self.stop_timer = False
                # Start tracking the song
                self.track_song()
                # Start update task
                self.update_status()

    def update_status(self):
        """Sends constant updates to the server every 3 seconds,
        and removes the track from the queue, once it has finished.
        """
        # If stop_timer is set, then return causing the loop to break
        if self.stop_timer:
            return

        # Always ensure there is a track to update on.
        if self.track.get('track') and self.track['track']:
            if self.core.playback.current_track.get():
                kwargs = {
                    'queue_id': self.queue,
                    'state': self.core.playback.state.get(),
                    'time_position': self.core.playback.time_position.get(),
                }
                self.session.update_head(kwargs)

        self.update_timer = threading.Timer(3, self.update_status)
        self.update_timer.start()

    def track_song(self):
        """Tracks the current playing track, and sends a pop request to the session,
        to remove the current track from the queue and fetch the next track.
        """
        # If stop_timer is set, then return causing the loop to break
        if self.stop_timer:
            return

        if self.track.get('track'):
            # Work out the time remaining on the track
            if self.track['track']['duration_ms'] is not None:
                t_end = self.track['track']['duration_ms']
                t_current = self.core.playback.time_position.get()
                time_til_end = t_end - t_current

                # If there is less than 5 seconds left on the track,
                # add the next track to the tracklist
                if time_til_end < 5000:
                    # Stop the timers
                    self.stop_timer = True
                    # Setup next track
                    return self._next_track()

        self.track_timer = threading.Timer(0.5, self.track_song)
        self.track_timer.start()

    def _next_track(self):
        """Fetches the next available track from the server,
        if no track is found, it will keep looping until a track is loaded in
        """
        kwargs = {'queue_id': self.queue}
        self.track = self.session.pop_head(kwargs)
        if self.track.get('track') and self.track['track']:
            self.queue = self.track['queue']
            return self._play_track()

        self.playback_timer = threading.Timer(1, self._next_track)
        self.playback_timer.start()

    def _play_track(self):
        """Starts the track using its uri parameter.
        If the track has a time_position property set,
        then seek the track to that position.
        """
        # Add track to tracklist
        self.core.tracklist.add(uri=self.track['track']['uri'])
        # Ensure a track is playing
        if self.core.playback.state.get() != 'playing':
            self.core.playback.play()

        if self.track['time_position'] and self.track['time_position'] > 500:

            if self.track['time_position'] + 1500 >= self.track['track']['duration_ms']:
                return self._next_track()

            self.core.playback.pause()
            seek_time = self.track['time_position'] + 1500
            # Delay required to allow mopidy to update,
            # before re-starting the track.
            time.sleep(1.5)
            self.core.playback.seek(seek_time)
