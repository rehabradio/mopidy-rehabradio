# Mopidy-rehabradio - Raspberry Pi setup

Simple instructions to get a Raspberry Pi setup with Mopidy music server and the mopidy-rehabradio extension installed

Setup
=============

Open up a terminal from your raspbery pi, and install git:

    $ sudo apt-get install -y git
    $ git clone https://github.com/rehabradio/mopidy-rehabradio.git ~/mopidy-rehabradio && cd ~/mopidy-rehabradio

Most of the set up and installation has been automated for you, through the `Makefile`:

    $ make install

This will install the Mopidy server and some third-party extensions (spotify/soundcloud/reahradio).
It will also create a `mopidy.conf` at `~/.config/mopidy`

Once the `make install` command has finished, open up the `mopidy.conf` file in a text editor. You will need to update some of the settings:

You can find the values for spotify and soundcloud here:

- [Spotify](https://www.spotify.com/uk/account/set-device-password/)
- [Soundcloud](http://www.mopidy.com/authenticate)

*Note that the spotify username and password values are not your noraml login values

The webhook values are taken from the api server that the webhook will be listening to, such as [rehabradio](https://github.com/rehabradio/server-core)

The `webhook` value is your api server url (www.your-domail.com/api/)
The `token` value is then created from your api server admin section. Login into the admin section and under the "players" section create a new user.
Once the user is created, you will be able to get your token


`mopidy.conf` file changes:

    [spotify]
    enabled = true
    username = [USERNAME]
    password = [PASSWORD]

    [soundcloud]
    enabled = true
    #explore_songs = 25
    auth_token = [AUTH-TOKEN]

    [webhook]
    enabled = true
    token = [PLAYER-TOKEN]
    webhook = [ROOT-API-URL]


Running
=============

To run the Mopidy server, run `mopidy` from inside a terminal

Startup Daemon
=============

If you are wanting to create a startup daemon to automate starting the mopidy server, each time your device boots then you can run::

    $ make daemon


Project resources
=================

- [Source code](https://github.com/rehabradio/mopidy-rehabradio)
