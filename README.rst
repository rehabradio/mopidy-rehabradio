****************************
Mopidy-Webhook
****************************

.. image:: https://img.shields.io/travis/rehabradio/mopidy-webhook/master.png?style=flat
    :target: https://travis-ci.org/rehabradio/mopidy-webhook
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/rehabradio/mopidy-webhook/master.svg?style=flat
   :target: https://coveralls.io/r/rehabradio/mopidy-webhook?branch=master
   :alt: Test coverage

Mopidy webhook extension

This is very much a work in progress. Please treat it as such and file issues where appropriate.


Configuration
=============
The set up process has been automated for you, simply pull down this repo and run_::

    $ make build

This will install mopidy, along with the spotify, soundcloud and youtube modules.
A config file will be place at `~/.config/mopidy/mopidy.conf`, which you will be required to manually update.
So go into the `mopidy.conf` file and replace the values below

    $ vi ~/.config/mopidy/mopidy.conf

    [spotify]
    # https://www.spotify.com/uk/account/set-device-password/
    username = [ device username ]
    password = [ password ]

    [soundcloud]
    # http://www.mopidy.com/authenticate
    auth_token = [ auth_token ]

    [webhook]
    # http://server-core.herokuapp.com/admin/radio_players/player/
    token = [player token provided from the server-core]

If you are wanting to create a startup deamon to automate starting the mopidy server, each time your device boots then you can run_::

    $ make deamon

Project resources
=================

- `Source code <https://github.com/rehabradio/mopidy-webhook>`_
- `Issue tracker <https://github.com/rehabradio/mopidy-webhook/issues>`_
- `Download development snapshot <https://github.com/rehabradio/mopidy-webhook/archive/master.tar.gz#egg=Mopidy-Webhook-dev>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
