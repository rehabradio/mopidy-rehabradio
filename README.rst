****************************
Mopidy-rehabradio
****************************

.. image:: https://travis-ci.org/rehabradio/mopidy-rehabradio.png
   :target: https://travis-ci.org/rehabradio/mopidy-rehabradio
   :alt: Latest Travis CI build status

.. image:: https://coveralls.io/repos/rehabradio/mopidy-rehabradio/badge.png
  :target: https://coveralls.io/r/rehabradio/mopidy-rehabradio?branch=develop
  :alt: Test coverage


Mopidy rehabradio extension

This is very much a work in progress. Please treat it as such and file issues where appropriate.


Configuration
=============

Most of the set up and installation has been automated for you, through the `Makefile`:

    $ make install

This will install the Mopidy server and some third-party extensions (spotify/soundcloud/reahradio).

A config file will be placed at `~/.config/mopidy/mopidy.conf`. You will need to update this with your webhook, spotify and soundcloud settings:

    vi ~/.config/mopidy/mopidy.conf

You can find the values for spotify and soundcloud here:

- [Spotify](https://www.spotify.com/uk/account/set-device-password/)
- [Soundcloud](http://www.mopidy.com/authenticate)

*Note that the spotify username and password values are not your noraml login values

The webhook values are taken from the api server that the webhook will be listening to, such as [rehabradio](https://github.com/rehabradio/server-core)

The `webhook` value is your api server url (www.your-domail.com/api/)
The `token` value is then created from your api server admin section. Login into the admin section and under the "players" section create a new user.
Once the user is created, you will be able to get your token

Running `mopidy` in your terminal, you should now see "webhook", "spotify", "soundcloud" and "youtube" loaded in the "Enabled extensions" output from the server, with no errors.

    INFO Starting Mopidy 0.18.3
    INFO Loading config from: builtin defaults, /etc/xdg/mopidy/mopidy.conf, /home/pi/.config/mopidy/mopidy.conf, command line options
    INFO Enabled extensions: mpd, http, stream, soundcloud, spotify, webhook, youtube
    INFO Disabled extensions: local

*Note some times there can be issues with soundcloud and spotify. If these do not appear in the loaded extensions, then install them via pip

    sudo pip install Mopidy-Spotify
    sudo pip install Mopidy-SoundCloud


Running
=============

To run the Mopidy server, run `mopidy` from inside a terminal


Startup Daemon
=============

If you are wanting to create a startup daemon to automate starting the mopidy server, each time your device boots then you can run::

    $ make daemon


Project resources
=================

- `Source code <https://github.com/rehabradio/mopidy-rehabradio>`_
- `Issue tracker <https://github.com/rehabradio/mopidy-rehabradio/issues>`_
- `Download development snapshot <https://github.com/rehabradio/mopidy-rehabradio/archive/master.tar.gz#egg=Mopidy-rehabradio-dev>`_


Changelog
=========

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
