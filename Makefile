help:
	@echo "build - Install mopidy and dependencies"
	@echo "deamon - Create a startup deamon to run mopidy on boot"
	@echo "test - Run test suite"

build:
	mkdir -p ~/.config/mopidy/

	wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
	sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/mopidy.list
	sudo apt-get update
	sudo apt-get install -y mopidy

	apt-cache search mopidy
	apt-get install -y bash git mopidy mopidy-spotify mopidy-soundcloud dbus icecast2 nfs-common nfs-client
	python setup.py develop

	pip install Mopidy-Spotify
	pip install Mopidy-Soundcloud
	pip install Mopidy-Youtube

	wget -O ~/.config/mopidy/mopidy.conf https://gist.githubusercontent.com/mjmcconnell/9de101676acfdb67d265/raw/d6f857154f0c925107574395ef8929951982f0c1/mopidy.conf

run:
	mopidy --config ~/.config/mopidy/mopidy.conf

deamon:
	cd /etc/init.d/
	sudo wget -O mopidy https://gist.githubusercontent.com/mjmcconnell/893201da1f6512247cc4/raw/960d296fa19418dd365591fad834aa9d977eb726/mopidy.daemon
	sudo chmod +x /etc/init.d/mopidy
	sudo service mopidy start
	sudo update-rc.d mopidy enable
