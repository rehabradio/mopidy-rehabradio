help:
	@echo "build - Install mopidy and dependencies"
	@echo "deamon - Create a startup deamon to run mopidy on boot"
	@echo "test - Run test suite"

install:
	apt-get update
	apt-get install -y python-setuptools python-pip python-dev build-essential
	pip install --upgrade pip

	wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
	wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/mopidy.list

	apt-get update
	apt-get install -y mopidy

	pip install Mopidy-Spotify
	pip install Mopidy-SoundCloud

	python setup.py develop

	mkdir -p ~/.config/mopidy/
	wget -O ~/.config/mopidy/mopidy.conf https://gist.githubusercontent.com/mjmcconnell/9de101676acfdb67d265/raw/1596ac2e732d36f8f1697130352ecd5a4e0df298/mopidy.conf

daemon:
	cd /etc/init.d/
	wget -O mopidy https://gist.githubusercontent.com/mjmcconnell/893201da1f6512247cc4/raw/960d296fa19418dd365591fad834aa9d977eb726/mopidy.daemon
	chmod +x /etc/init.d/mopidy
	service mopidy start
	update-rc.d mopidy enable
