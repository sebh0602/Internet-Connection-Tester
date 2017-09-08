#internet tester
import socket
import time
import os
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

        global successful_attempts
        successful_attempts=0
        global failures
        failures=0
        global consecutive_success
        consecutive_success=0
        global best_consec
        best_consec=0

        while True:
                try:
                        s=socket.socket()
                        s.connect(("google.com",80))

                        successful_attempts+=1
                        consecutive_success+=1

                        if consecutive_success>best_consec:
                                best_consec=consecutive_success


                except:
                        failures+=1
                        consecutive_success=0

                os.system("clear")
                display()
                time.sleep(1)

def display():
        total=successful_attempts+failures

        print("Internet connection tester\n" + "-"*26 + "\n")
        print("Total attempts:",total)
        print("Successes:     ",successful_attempts,round(successful_attempts/total*100,4),"%")
        print("Failures:      ",failures,round(failures/total*100,4),"%")
        print("Best:          ",best_consec)
        print()
        print("Running for:   ",round(time.time()-start_time,1),"seconds")

run()
