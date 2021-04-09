#internet tester
#pip install speedtest-cli [--upgrade]
import socket
import time
import os
import sys
import threading


def now():
	return time.localtime(time.time())

def dateTime():
	n = now()
	year = n.tm_year

	month = n.tm_mon
	if month < 10:
		month = "0" + str(month)

	day = n.tm_mday
	if day < 10:
		day = "0" + str(day)

	hour = n.tm_hour
	if hour < 10:
		hour = "0" + str(hour)

	minute = n.tm_min
	if minute < 10:
		minute = "0" + str(minute)

	second = n.tm_sec
	if second < 10:
		second = "0" + str(second)

	return "{0}-{1}-{2} {3}:{4}:{5}".format(year,month,day,hour,minute,second)

saveDir = "results_{0}".format(dateTime().split(" ")[0])

def run():
	inst=mainThread()
	inst.daemon=True
	inst.start()

	input()

class mainThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		connectionTester()

def connectionTester():
	if not os.path.exists(saveDir):
		os.mkdir(saveDir)
	if not os.path.exists(saveDir + "/results_speedtest.txt"):
		with open(saveDir + "/results_speedtest.txt","w+") as file:
			file.write("")
	if not os.path.exists(saveDir + "/errors.txt"):
		with open(saveDir + "/errors.txt","w+") as file:
			file.write("")

	global start_time
	start_time=time.time()

	global successes
	successes=0

	global failures
	failures=0

	global consecutive_success
	consecutive_success=0

	global best_consec
	best_consec=0

	global ping_sum
	ping_sum = 0 #(ms)

	global worst_ping
	worst_ping = 0

	while True:
		if (successes + failures)%900 == 0:
			speedtestThread().start()

		try:
			s=socket.socket()
			st = time.perf_counter()
			s.connect(("8.8.8.8",53))
			et = time.perf_counter()

			ping = round((et-st)*1000)
			ping_sum += ping
			if ping > worst_ping:
				worst_ping = ping
			if ping > 1000:
				warning("p",ping)

			successes+=1
			consecutive_success+=1

			if consecutive_success>best_consec:
				best_consec=consecutive_success


		except:
			failures+=1
			consecutive_success=0
			error("p")

		display()
		time.sleep(0.95)

def warning(type,data):
	with open(saveDir + "/errors.txt","a") as file:
		dT = dateTime()
		if type == "p":
			file.write("{0}: WARNING - {1}ms ping\n".format(dT,data))
		elif type == "ps":
			file.write("{0}: WARNING - {1}ms ping (speedtest)\n".format(dT,data))
		elif type == "d":
			file.write("{0}: WARNING - {1}mbps down\n".format(dT,data))
		elif type == "u":
			file.write("{0}: WARNING - {1}mbps up\n".format(dT,data))

def error(type):
	with open(saveDir + "/errors.txt","a") as file:
		dT = dateTime()
		if type == "p":
			file.write("{0}: ERROR - connection not possible\n".format(dT))
		else:
			file.write("{0}: ERROR - speedtest failed\n".format(dT))


def display():
	total=successes+failures

	os.system('cls' if os.name == 'nt' else 'clear')

	txt = ""
	txt += "Internet connection tester\n" + "-"*26 + "\n"
	txt += "\nTotal attempts: " + str(total)
	txt += "\nSuccesses:      " + str(successes) + " (" +str(round(successes/total*100,2)) + " %)"
	txt += "\nFailures:       " + str(failures) + " (" +str(round(failures/total*100,2)) + " %)"
	txt += "\nBest consec.:   " + str(best_consec)
	txt += "\n"
	if ping_sum > 0:
		txt += "\nAvg. ping:      " + str(round(ping_sum/successes,1)) + "ms"
		txt += "\nWorst ping:     " + str(worst_ping) + "ms"
		txt += "\n"
	txt += "\nRunning for:    " + str(round(time.time()-start_time,1)) + " seconds"

	print(txt)
	try:
		with open(saveDir + "/results.txt", "w") as file:
			file.write(txt)
	except:
		pass


class speedtestThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		try:
			import speedtest
			spdt = speedtest.Speedtest()
			spdt.get_best_server()
			spdt.download()
			spdt.upload()
			results = spdt.results.dict()

			dT = dateTime()
			down = round(results["download"]/1000000,1)
			up = round(results["upload"]/1000000,1)
			ping = round(results["ping"])

			if down < 10:
				warning("d",down)
			if up < 2:
				warning("u",up)
			if ping > 1000:
				warning("ps",ping)

			txt = ""
			txt += "{0}, host: {1}, {2}".format(dT,results["server"]["sponsor"], results["server"]["name"])
			txt += "\n{0} ms ping".format(ping)
			txt += "\n{0} mbps down".format(down)
			txt += "\n{0} mbps up".format(up)
			txt += "\n\n"
		except:
			txt = dateTime() + ": Speedtest error\n\n"
			error("s")

		try:
			with open(saveDir + "/results_speedtest.txt","a") as file:
				file.write(txt)
		except:
			pass


run()
