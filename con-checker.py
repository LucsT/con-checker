#!/usr/bin/python

import os
import datetime
import sys
import signal
import time
from config import *

def check_ip(ip, number=1, time_out=PING_TIMEOUT):
    '''
    Return nothing if 'Number' ping with 'Timeout' is OK
    '''
    return os.system("ping -c %s -W %s %s 1>/dev/null 2>&1" %(number, 
                                                          time_out, ip))

def log(string):
    '''
    Log in file and print on console
    '''
    sys.stdout.write('%s' %string)
    try:
        file = open(LOG_FILE,"a")
    except:
        #Create if not exist
        file = open(LOG_FILE,"w")
    file.write(string)
    file.close()

def wait_back_online(delay=1):
    '''
    Wait until one IP is up
    '''
    while check_ip(IPONLINE1) and check_ip(IPONLINE2):
        time.sleep(delay)


def main():
    printup_delay = 0
    now = datetime.datetime.now()
    log("Start at : %s\n" % now.strftime("%Y-%m-%d %H:%M:%S"))

    while(1):
        ip1_state = check_ip(IPONLINE1)
        ip2_state = check_ip(IPONLINE2)
        down = datetime.datetime.now()
        #IP1 is Down and IP2 is Down
        if ip1_state and ip2_state:
            router_state = check_ip(IPROUTER)
            #If you can't contact your router, it's your network problem
            if router_state:
                log("%s UNREACHABLE Router/Box\n" 
                    % down.strftime("%Y-%m-%d %H:%M:%S"))
                wait_back_online()
                up = datetime.datetime.now()
                delay = (up - down)
                log("%s Router back after %s Seconds\n" 
                    %(up.strftime("%Y-%m-%d %H:%M:%S"),
                      delay.seconds))
                os.system("sleep 1")

            #You can contact your router, so internet is down
            else:
                log("%s DOWN\n" % down.strftime("%Y-%m-%d %H:%M:%S"))
                wait_back_online()
                up = datetime.datetime.now()
                delay = (up - down)
                log("%s UP after %s Seconds\n" 
                    %(up.strftime("%Y-%m-%d %H:%M:%S"), delay.seconds))

        #IP1 is down
        elif ip1_state and not ip2_state:
            log("%s Lost ping :" % down.strftime("%Y-%m-%d %H:%M:%S") \
                    +" GOOGLE seems down and OpenDNS not\n" )

        #IP2 is down
        elif not ip1_state and ip2_state:
            log("%s Lost ping :" % down.strftime("%Y-%m-%d %H:%M:%S") \
                    +" OpenDNS seems down and Google not\n")

        #Everything is OK
        else:
            printup_delay -= 1
            if printup_delay < 0:
                printup_delay = 600
                down = datetime.datetime.now()
                log("%s UP \n" % down.strftime("%Y-%m-%d %H:%M:%S"))
            #Wait the delay and go on another time!
            time.sleep(DELAY)
        
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted by user, exiting'
        sys.exit(1)
        
