# Mopidy-rehabradio - Raspberry Pi setup

Simple instructions to get a Raspberry Pi setup with Mopidy music server and the mopidy-rehabradio extension installed

This setup is designed for a Raspberry Pi b+ model, with Raspbian os installed

Setup
=============

Open up a terminal from your raspbery pi, and install git:

    $ git clone https://github.com/rehabradio/mopidy-rehabradio.git ~/mopidy-rehabradio && cd ~/mopidy-rehabradio

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

    $ sudo dpkg-reconfigure mopidy

And select the option to start the mopidy server from boot.

Unfortunately the built-in daemon does not load your local config file, so we have to add the path to the daemon fle:

    sudo vi /etc/init.d/mopidy

And update the `CONFIG_FILES` value to:

    CONFIG_FILES="/usr/share/mopidy/conf.d:/etc/mopidy/mopidy.conf:/home/pi/.config/mopidy/mopidy.conf"

