import os
import datetime

#Google DNS
IPONLINE1="8.8.8.8"
#Open DNS
IPONLINE2="37.59.47.6"
#Your router
IPROUTER="192.168.0.1"
#Name of logging file
LOG_FILE="statut.log"
# Delay between ping in seconds
DELAY="2"

def check_ip1(number=1, time_out=2):
    return os.system("ping -c %s -W %s %s >> /dev/null" %(number, time_out, IPONLINE1))

def check_ip2(number=1, time_out=2):
    return os.system("ping -c %s -W %s %s >> /dev/null" %(number, time_out, IPONLINE2))

def check_router(number=1, time_out=2):
    return os.system("ping -c %s -W %s %s >> /dev/null" %(number, time_out, IPROUTER))


def log(string):
      print(string)
      try:
          file = open(LOG_FILE,"a")
      except:
          file = open(LOG_FILE,"w")
      file.write(string)
      file.close()

def wait_ip1_online(delay=1):
    while check_ip1():
        os.system("sleep %s" % delay)
    

#Start message with a blank line
big_delay = 0
now = datetime.datetime.now()
log(" \nStart at : %s\n" % now.strftime("%Y-%m-%d %H:%M:%S"))

while(1):
    if check_ip1():
        down = datetime.datetime.now()
	ip2_state = check_ip2()
	routeur_state = check_router()
	#Temporisation
        os.system("sleep 1")
	down2 = datetime.datetime.now()
        if check_ip1():
            #If ip1 is out, check ip2
            if not ip2_state:
                log("%s GOOGLE seems down and OpenDNS not\n" % down.strftime("%Y-%m-%d %H:"\
                                                               + "%M:%S"))
		log("%s GOOGLE seems down and Second Test server not\n" % down2.strftime("%Y-%m-%d %H:"\
                                                               + "%M:%S"))

            elif routeur_state:
            #If you can't contact your router, it's your network problem
                log("%s UNREACHABLE\n" % down.strftime("%Y-%m-%d %H:%M:%S"))
                wait_ip1_online()
                up = datetime.datetime.now()
                delay = (up - down)
                log("%s UP after %s Seconds\n" %(up.strftime("%Y-%m-%d %H:"\
						 + "%M:%S"), delay.seconds))
            else:
            #If you're still reach your router, connection problem
                log("%s DOWN\n" % down.strftime("%Y-%m-%d %H:%M:%S"))
                wait_ip1_online()
                up = datetime.datetime.now()
                delay = (up - down)
                log("%s UP after %s Seconds\n" %(up.strftime("%Y-%m-%d %H:"\
	                                         + "%M:%S"), delay.seconds))
        #else it's just a lost packet
        else:
            log("%s Packets loss\n" % down.strftime("%Y-%m-%d %H:%M:%S"))    
    
    big_delay -= 1
    if big_delay < 0:
        big_delay = 600
        now = datetime.datetime.now()
        log("%s UP \n" % now.strftime("%Y-%m-%d %H:%M:%S"))
    #Wait the delay and go on!
    os.system("sleep %s" % DELAY)

