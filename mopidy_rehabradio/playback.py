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
    """

    queue = None
    track = None
    next_track = None
    stop_update_thread = True
    stop_track_thread = True

    def __init__(self, config, core, session):
        super(WebhookPlayback, self).__init__()
        self.config = config
        self.core = core
        self.core.tracklist.consume = True
        self.session = session

    def on_start(self):
        """Grab the current head track, and add it to the tracklist.
        Starts the play method.
        """
        self.initiate()

    def initiate(self):
        """Loads in the top track of a given queue.
        Note will loop itself every second until a track is loaded.
        """
        self.track = self.session.fetch_head()

        if self.track.get('track') is None:
            time.sleep(1)
            return self.initiate()

        self.queue = self.track['queue']
        self.core.tracklist.add(uri=self.track['track']['uri'])

        self.play()

    def on_stop(self):
        """Stops the playback of the current track,
        and cleans up all the treads and tracklist.
        """
        # Stop playback
        self.core.playback.stop()
        # Stop any new timers
        self.stop_update_thread = True
        self.stop_track_thread = True
        # Empty queue
        self.core.tracklist.clear()

    def on_event(self, event):
        """Fires functions base of mopidy tracklist events
        """
        state = self.core.playback.state.get()

        if event == 'tracklist_changed' and state == 'stopped':
            return self.next()

    def play(self):
        """Starts playing the first track in the tracklist.
        If the track has a "time_position" value then seek the track to that postion.
        """
        # Start track
        self.core.playback.play()

        # Annoyingly cant start a track at a given time,
        # So once the track has started we can seek it to the correct position
        if self.track['time_position']:
            self.seek()

        self.stop_update_thread = False
        self.stop_track_thread = False
        self.update_thread()
        self.track_thread()

    def seek(self):
        """Seeks a track to a given location.
        Note there is a 1.5 second delay to allow mopidy to settle.
        """
        seek_time = self.track['time_position'] + 2000
        # If the seeked time is longer than the tracks duration,
        # then start the next track instead
        if seek_time >= self.track['track']['duration_ms']:
            return self.next()
        # Delay required to allow mopidy to setup track
        time.sleep(1.5)
        self.core.playback.seek(seek_time)

    def next(self):
        """Plays the next track which is stored locally.
        If no track is found then it loops every second until a track is found.
        """
        if self.next_track is None:
            time.sleep(1)
            return self.next()

        self.track = self.next_track
        self.next_track = None

        self.core.tracklist.add(uri=self.track['track']['uri'])
        self.play()

    def update_thread(self):
        """Sends updates to the server every 3 seconds
        on the status of the playing track.
        """
        # If stop_thread is set, then return causing the loop to break
        if self.stop_update_thread:
            return

        # Ensure there is a track to report on
        if self.core.playback.current_track.get():
            # Ensure track has started and that it is also not about to end.
            time_position = self.core.playback.time_position.get()
            total = self.track['track']['duration_ms']
            if 1000 < time_position < (total - 9000):
                # Send updates to the server
                kwargs = {
                    'track_id': self.track['id'],
                    'queue_id': self.queue,
                    'state': self.core.playback.state.get(),
                    'time_position': self.core.playback.time_position.get(),
                }
                self.session.update_head(kwargs)

        # Loop method every 3 seconds
        thread_timer = threading.Timer(3, self.update_thread)
        thread_timer.start()

    def track_thread(self):
        """Watches the track to know when to trigger fetching a the next track.
        """
        # If stop_thread is set, then return causing the loop to break
        if self.stop_track_thread:
            return

        if self.track.get('track'):
            # Work out the time remaining on the track
            if self.track['track']['duration_ms'] is not None:
                t_end = self.track['track']['duration_ms']
                t_current = self.core.playback.time_position.get()
                time_til_end = t_end - t_current

                # If there is less than 5 seconds left on the track,
                # add the next track to the tracklist,
                # or if no track is currently playing
                if time_til_end < 5000 or not self.core.playback.current_track.get():
                    # Stop updates
                    self.stop_update_thread = True

                    # Fetch next track
                    kwargs = {'queue_id': self.queue}
                    next_track = self.session.pop_head(kwargs)

                    # Don't exit loop until a new track is loaded in.
                    if next_track.get('track'):
                        self.next_track = next_track
                        self.queue = self.next_track['queue']
                        # Exit loop
                        return

        # Loop method every 1/2 second
        thread_timer = threading.Timer(0.5, self.track_thread)
        thread_timer.start()
