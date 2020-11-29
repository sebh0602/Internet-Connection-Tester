#internet tester
import socket
import time
import os
import sys
import threading

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
	if not os.path.exists("results_speedtest.txt"):
		with open("results_speedtest.txt","w+") as file:
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

	parse_arguments()

	while True:
		if (successes + failures)%900 == 0:
			speedtestThread().start()

		try:
			s=socket.socket()
			s.connect(("8.8.8.8",53))

			successes+=1
			consecutive_success+=1

			if consecutive_success>best_consec:
				best_consec=consecutive_success


		except:
			failures+=1
			consecutive_success=0

		display()
		time.sleep(0.95)


class speedtestThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		#try:
		import speedtest
		spdt = speedtest.Speedtest()
		spdt.get_best_server()
		spdt.download()
		spdt.upload()
		results = spdt.results.dict()
		txt = ""
		txt += "{0}, host: {1}, {2}".format(results["timestamp"][:19].replace("T"," "),results["server"]["sponsor"], results["server"]["name"])
		txt += "\n{0} ms ping".format(round(results["ping"]))
		txt += "\n{0} mbps down".format(round(results["download"]/1000000,1))
		txt += "\n{0} mbps up".format(round(results["upload"]/1000000,1))
		txt += "\n\n"
		#except:
		#	txt = "Speedtest error\n\n"

		try:
			with open("results_speedtest.txt","r+") as file:
				f = file.read()
				file.write(f + txt)
		except:
			pass

def parse_arguments():
	args=sys.argv
	l=len(args)-1

	if l>=1: #L==one
		try:
			global successes
			successes=int(args[1])
		except ValueError:
			pass

	if l>=2:
		try:
			global failures
			failures=int(args[2])
		except ValueError:
			pass

	if l>=3:
		try:
			global best_consec
			best_consec=int(args[3])
		except ValueError:
			pass

	if l>=4:
		try:
			global start_time
			start_time-=float(args[4])
		except ValueError:
			pass

def display():
	total=successes+failures

	os.system('cls' if os.name == 'nt' else 'clear')

	txt = ""
	txt += "Internet connection tester\n" + "-"*26 + "\n"
	txt += "\nTotal attempts: " + str(total)
	txt += "\nSuccesses:      " + str(successes) + " (" +str(round(successes/total*100,4)) + " %)"
	txt += "\nFailures:       " + str(failures) + " (" +str(round(failures/total*100,4)) + " %)"
	txt += "\nBest:           " + str(best_consec)
	txt += "\n"
	txt += "\nRunning for:    " + str(round(time.time()-start_time,1)) + " seconds"

	print(txt)
	try:
		with open("results.txt", "w") as file:
			file.write(txt)
	except:
		pass

run()
