# README #

	This program can be run on your PC or server using Python 3.
	In its current configuration, it tries to connect to Google's DNS server once every second to test if the internet connection is working.
	I use it to monitor Linux server uptime (assuming Google's server is up too of course). For this purpose I have it run in the background, and check in on it every once in a while.

	To quit, press return.
	If you want to add parameters, run:
	filename.py successes failures best seconds

	speedtest-cli needs to be installed for this to work.

	All results are saved to results.txt and results_speedtest.txt respectively
