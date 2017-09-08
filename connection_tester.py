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
		try:
			s=socket.socket()
			s.connect(("google.com",80))

			successes+=1
			consecutive_success+=1

			if consecutive_success>best_consec:
				best_consec=consecutive_success


		except:
			failures+=1
			consecutive_success=0

		display()
		time.sleep(1)

		
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
	
	print("Internet connection tester\n" + "-"*26 + "\n")
	print("Total attempts:",total)
	print("Successes:     ",successes,round(successes/total*100,4),"%")
	print("Failures:      ",failures,round(failures/total*100,4),"%")
	print("Best:          ",best_consec)
	print()
	print("Running for:   ",round(time.time()-start_time,1),"seconds")

run()
