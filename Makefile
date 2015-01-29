help:
	@echo "build - Install mopidy and dependencies"
	@echo "deamon - Create a startup deamon to run mopidy on boot"
	@echo "test - Run test suite"

install:
	sudo apt-get update
	sudo apt-get install -y python-setuptools python-pip python-dev build-essential
	sudo pip install --upgrade pip

	wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
	wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/mopidy.list

	sudo apt-get update
	sudo apt-get install -y mopidy

	sudo apt-get install -y mopidy-spotify
	sudo apt-get install -y mopidy-soundcloud

	sudo pip install Mopidy-Spotify
	sudo pip install Mopidy-SoundCloud

	sudo python setup.py install

	mkdir -p ~/.config/mopidy/
	wget -O ~/.config/mopidy/mopidy.conf https://gist.githubusercontent.com/mjmcconnell/9de101676acfdb67d265/raw/1596ac2e732d36f8f1697130352ecd5a4e0df298/mopidy.conf

daemon:
	cd /etc/init.d/
	wget -O mopidy https://gist.githubusercontent.com/mjmcconnell/893201da1f6512247cc4/raw/960d296fa19418dd365591fad834aa9d977eb726/mopidy.daemon
	chmod +x /etc/init.d/mopidy
	service mopidy start
	update-rc.d mopidy enable
