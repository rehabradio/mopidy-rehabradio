# future imports
from __future__ import unicode_literals

# stdlib imports
import logging
import os

# third-party imports
from mopidy import config, ext

# local imports
from .frontend import WebhookFrontend

__version__ = '0.1.0'
logger = logging.getLogger(__name__)


class Extension(ext.Extension):

    dist_name = 'Mopidy-rehabradio'
    ext_name = 'webhook'
    version = __version__

    def get_default_config(self):
        conf_file = os.path.join(os.path.dirname(__file__), 'ext.conf')
        return config.read(conf_file)

    def get_config_schema(self):
        schema = super(Extension, self).get_config_schema()
        schema['token'] = config.Secret()
        schema['webhook'] = config.String()
        return schema

    def setup(self, registry):
        registry.add('frontend', WebhookFrontend)
