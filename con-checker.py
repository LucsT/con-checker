import os
import datetime


IPONLINE1="8.8.8.8"
IPONLINE2="89.2.0.1"
IPROUTER="192.168.0.1"
LOG_FILE="statut.log"
# Delay between ping in seconds
DELAY="5"

def check_ip1():
    return os.system("ping -c 1 %s >> /dev/null" % IPONLINE1)

def check_ip2():
    return os.system("ping -c 1 %s >> /dev/null" % IPONLINE2)

def check_router():
    return os.system("ping -c 1 %s >> /dev/null" % IPROUTER)

def log(string):
      print(string)
      try:
          file = open(LOG_FILE,"a")
      except:
          file = open(LOG_FILE,"w")
      file.write(string)
      file.close()

def wait_ip1_online():
    while check_ip1:
        os.system("sleep %s" % DELAY)
    

#Start message with a blank line
big_delay = 0
now = datetime.datetime.now()
log(" \nStart at : %s\n" % now.strftime("%Y-%m-%d %H:%M:%S"))

while(1):
    if check_ip1():
        down = datetime.datetime.now()
        #If ip1 is out, check ip2
        if not check_ip2():
            log("%s GOOGLE seems down!!\n" % down.strftime("%Y-%m-%d %H:"\
                                                               + "%M:%S"))
        #Temporisation
        os.system("sleep 1")
        #If you're still reach your router, connection problem
        if check_ip1() and not check_router():
            log("%s DOWN\n" % down.strftime("%Y-%m-%d %H:%M:%S"))
            wait_ip1_online()
            up = datetime.datetime.now()
            delay = (up - down)
            log("%s UP after %s \n" %(up.strftime("%Y-%m-%d %H:%M:%S"),
                                      delay.strftime("%H:%M:%S")))
        #If you can't contact your router, it's your network problem
        elif check_ip1() and check_router():
            log("%s UNREACHABLE\n" % down.strftime("%Y-%m-%d %H:%M:%S"))
            wait_ip1_online()
            up = datetime.datetime.now()
            delay = (up - down)
            log("%s UP after %s \n" %(up.strftime("%Y-%m-%d %H:%M:%S"),
                                      delay.strftime("%H:%M:%S")))
        #else it's just a lost packet
        else:
            log("%s 1 packet loss\n" % now.strftime("%Y-%m-%d %H:%M:%S"))    
    
    big_delay -= 1
    if big_delay < 0:
        big_delay = 600
        now = datetime.datetime.now()
        log("%s UP \n" % now.strftime("%Y-%m-%d %H:%M:%S"))
    #Wait the delay and go on!
    os.system("sleep 5")

