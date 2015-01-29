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

Once the `make install` command has finished, run `mopidy` in the terminal to start the mopidy server.
Note that you will get errors in regards to spotify and soundcloud. The purpose of doing this first is to create the `mopidy.conf` file.
Stop the server with Ctrl-C.

Now we edit the newly created `.conf` file, updating the spotify and soundcloud settings:

    vim ~/.config/mopidy/mopidy.conf

You can find the values for spotify and soundcloud here:

- [Spotify](https://www.spotify.com/uk/account/set-device-password/)
- [Soundcloud](http://www.mopidy.com/authenticate)

*Note that the spotify username and password values are not your noraml login values

Running `mopidy` again, you should now see "spotify" and "soundcloud" loaded in the "Enabled extensions" output from the server, with no errors.

    INFO Starting Mopidy 0.18.3
    INFO Loading config from: builtin defaults, /etc/xdg/mopidy/mopidy.conf, /home/pi/.config/mopidy/mopidy.conf, command line options
    INFO Enabled extensions: mpd, http, stream, soundcloud, spotify
    INFO Disabled extensions: local


Now to setup the webhook. run `sudo python setup.py develop`. This will install the mopidy-rehabradio extension to your system.
Once it has install go back into the `mopidy.conf` file and add some config values for the mopidy-rehabradio extension:

    [webhook]
    enabled = true
    token = [PLAYER-TOKEN]
    webhook = [ROOT-API-URL]

The webhook values are taken from the api server that the webhook will be listening to, such as [rehabradio](https://github.com/rehabradio/server-core)

The `webhook` value is your api server url (www.your-domail.com/api/)
The `token` value is then created from your api server admin section. Login into the admin section and under the "players" section create a new user.
Once the user is created, you will be able to get your token


Running
=============

To run the Mopidy server, run `mopidy` from inside a terminal


Startup Daemon
=============

If you are wanting to create a startup daemon to automate starting the mopidy server, each time your device boots then you can run::

    $ make daemon
