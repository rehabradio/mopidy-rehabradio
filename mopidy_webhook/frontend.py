# future imports
from __future__ import unicode_literals

# stdlib imports
import json
import logging
import time

# third-party imports
import pykka
import requests
from mopidy.core import CoreListener
from mopidy.models import ModelJSONEncoder


logger = logging.getLogger(__name__)


def _fetch_head_track_uri(webhook_url):
    response = requests.get(webhook_url)
    queue_track = response.json()
    track = queue_track['track']

    if (track['source_type'] == 'spotify'):
        track_uri = 'spotify:track:' + track['source_id']
    elif (track['source_type'] == 'soundcloud'):
        track_uri = 'soundcloud:song/' + track['name'] + '.' + track['source_id']
    elif (track['source_type'] == 'youtube'):
        track_uri = 'youtube:video/' + track['name'] + '.' + track['source_id']
    else:
        return None
    return track_uri


def _pop_head(webhook_url):
    logger.info('pop head called')
    return requests.delete(webhook_url)


def _send_webhook(class_name, webhook_url, event=None, **kwargs):
    logger.info('{0} Webhook URL: {1}'.format(class_name, webhook_url))

    payload = json.dumps(kwargs, cls=ModelJSONEncoder, indent=2)
    logger.info('{0} Webhook Payload: {1}'.format(class_name, payload))

    try:
        #response = requests.post(webhook_url, data=payload)
        raise
    except Exception as e:
        logger.warning('Unable to send {0} Webhook: ({1}) {2}'.format(
            class_name,
            e.__class__.__name__,
            e.message,
        ))
    else:
        logger.info('{0} Webhook Response Status: {1}'.format(class_name, response.status_code))
        logger.info('{0} Webhook Response Body: {1}'.format(class_name, response.text))


class StatusReporter(pykka.ThreadingActor):

    def __init__(self, config, core):
        super(StatusReporter, self).__init__()
        self.config = config
        self.core = core
        self.in_future = self.actor_ref.proxy()

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        self.report_status()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def report_status(self):
        webhook_url = self.config['webhook']['webhook']
        kwargs = {
            'current_track': self.core.playback.current_track.get(),
            'state': self.core.playback.state.get(),
            'time_position': self.core.playback.time_position.get(),
        }
        _send_webhook(self.__class__.__name__, webhook_url, **kwargs)
        time.sleep(2)
        self.in_future.report_status()


class EventReporter(pykka.ThreadingActor, CoreListener):

    def __init__(self, config, core):
        super(EventReporter, self).__init__()
        self.config = config

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def on_event(self, event, **kwargs):
        webhook_url = self.config['webhook']['webhook'] + event + '/'
        _send_webhook(self.__class__.__name__, webhook_url, event, **kwargs)


class TrackManager(pykka.ThreadingActor, CoreListener):

    def __init__(self, config, core):
        super(TrackManager, self).__init__()
        self.core = core
        self.config = config
        self.webhook_url = config['webhook']['webhook'] + 'head/'

    def on_start(self):
        logger.info('{0} actor started.'.format(self.__class__.__name__))
        # Grab the track at the top of the queue
        uri = _fetch_head_track_uri(self.webhook_url)
        # Add track to playlist
        self.core.tracklist.add(tracks=None, at_position=None, uri=uri)
        # Start track
        self.core.playback.play()

    def on_stop(self):
        logger.info('{0} actor stopped.'.format(self.__class__.__name__))

    def on_event(self, event, **kwargs):
        logger.info(event)
        if event == 'playlists_loaded':
            logger.info('track loaded')
        if event == 'tracklist_changed':
            logger.info('track changed')
        if event == 'track_playback_started':
            logger.info('track started')
        if event == 'seeked':
            logger.info('track seeked')
        if event == 'track_playback_paused':
            logger.info('track paused')
        if event == 'track_playback_resumed':
            logger.info('track resumed')
        if event == 'track_playback_ended':
            logger.info('track ended')
            response = _pop_head(self.webhook_url + 'pop/')
            logger.info(response)
            time.sleep(1)
            # Clean up tracklist
            self.core.tracklist.clear()
            # Grab the new track at the top of the queue
            uri = _fetch_head_track_uri(self.webhook_url)
            # Add track to playlist
            self.core.tracklist.add(tracks=None, at_position=None, uri=uri)
            # Start track new track
            self.core.playback.play()


class WebhookFrontend(pykka.ThreadingActor, CoreListener):

    def __init__(self, config, core):
        super(WebhookFrontend, self).__init__()
        self.config = config
        self.core = core
        self.event_reporter = None
        self.status_reporter = None
        self.webhook_url = config['webhook']['webhook'] + 'head/'

    def on_start(self):
        #self.event_reporter = EventReporter.start(self.config, self.core)
        #self.status_reporter = StatusReporter.start(self.config, self.core)
        self.track_reporter = TrackManager.start(self.config, self.core)

    def _stop_children(self):
        #self.event_reporter.stop()
        #self.status_reporter.stop()
        pass

    def on_stop(self):
        #self._stop_children()
        pass

    def on_failure(self, exception_type, exception_value, traceback):
        #self._stop_children()
        pass

    def track_playback_started(tl_track):
        #logger.info('track started')
        pass

    def track_playback_paused(self, tl_track, time_position):
        #logger.info('track paused')
        pass

    def track_playback_ended(self, tl_track, time_position):
        #logger.info('track ended')
        pass
