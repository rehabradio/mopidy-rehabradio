help:
	@echo "build - Install mopidy and dependencies"
	@echo "deamon - Create a startup deamon to run mopidy on boot"
	@echo "test - Run test suite"

install:
	sudo apt-get update
	sudo apt-get dist-upgrade
	sudo apt-get install -y python-setuptools python-pip python-dev build-essential

	wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
	sudo wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/mopidy.list

	sudo apt-get update
	sudo apt-get install -y mopidy

	sudo apt-get install -y mopidy-spotify
	sudo apt-get install -y mopidy-soundcloud

daemon:
	cd /etc/init.d/
	wget -O mopidy https://gist.githubusercontent.com/mjmcconnell/893201da1f6512247cc4/raw/960d296fa19418dd365591fad834aa9d977eb726/mopidy.daemon
	chmod +x /etc/init.d/mopidy
	service mopidy start
	update-rc.d mopidy enable
