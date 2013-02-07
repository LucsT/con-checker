import os
import datetime



try:
    file = open("status.log","a")
except:
    file = open("status.log","w")
now = datetime.datetime.now()
file.write("\nStart at : %s\n" % now.strftime("%Y-%m-%d %H:%M:%S"))
file.close()


while(1):
    #Si on perds google
    if os.system("ping -c 1 8.8.8.8 >> /dev/null"):
        #Ouverture du fichier log
        file = open("status.log","a")
        down = datetime.datetime.now()
        #On verifie si uniquement google est down
        if not os.system("ping -c 1 9.9.9.9 >> /dev/null"):
            print("GOOGLE seems down!!")
            file.write("%s GOOGLE seems down!!\n" % down.strftime("%Y-%m-%d %H:%M:%S"))
        #Temporisation
        os.system("sleep 1")
        # Si google out et box OK
        if os.system("ping -c 1 8.8.8.8 >> /dev/null") and not os.system("ping -c 1 192.168.0.1 >> /dev/null"):
            print("DOWN at %s" % down.strftime("%Y-%m-%d %H:%M:%S"))
            file.write("%s DOWN\n" % down.strftime("%Y-%m-%d %H:%M:%S"))
            #Attendre le retour de google
            while os.system("ping  -c 1 8.8.8.8 >> /dev/null"):
                os.system("sleep 5")
            up = datetime.datetime.now()
            delay = (up - down)
            file.write("%s UP \n" % up.strftime("%Y-%m-%d %H:%M:%S"))
            print("UP at %s after %s Seconds" % (up.strftime("%Y-%m-%d %H:%M:%S", delay.seconds)))
        # Si google out et box out
        elif os.system("ping -c 1 8.8.8.8 >> /dev/null") and os.system("ping -c 1 192.168.0.1 >> /dev/null"):
            file.write("%s LAN UNREACHABLE\n" % down.strftime("%Y-%m-%d %H:%M:%S"))
            while os.system("ping  -c 1 8.8.8.8 >> /dev/null"):
                #Do nothing, wait etablishement
                os.system("sleep 5")
            now = datetime.datetime.now()
            file.write("%s UP \n" % now.strftime("%Y-%m-%d %H:%M:%S"))
            print("UP at %s"  % now.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            file.write("%s 1 packet loss\n" % now.strftime("%Y-%m-%d %H:%M:%S"))    
        
        file.close()

    print("UP %s" % datetime.datetime.now())
    os.system("sleep 5")

file.close()
