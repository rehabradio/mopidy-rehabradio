help:
	@echo "install - Install mopidy and dependencies"

install:
	sudo apt-get update
	sudo apt-get dist-upgrade -y
	sudo apt-get install -y vim python-setuptools python-pip python-dev build-essential

	wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
	sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/mopidy.list

	sudo apt-get update
	sudo apt-get install -y mopidy

	sudo python setup.py install

	sudo apt-get install -y mopidy-spotify
	sudo apt-get install -y mopidy-soundcloud

	sudo pip install Mopidy-Youtube

	mkdir -p ~/.config/mopidy/
	wget -O ~/.config/mopidy/mopidy.conf https://gist.githubusercontent.com/mjmcconnell/9de101676acfdb67d265/raw/1596ac2e732d36f8f1697130352ecd5a4e0df298/mopidy.conf
