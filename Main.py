
from DB_Classes import *
from time import sleep
from time import time as timestamp
import RPi.GPIO as GPIO
import time, datetime, os, serial
import getpass

techs = user_DB("RME_Users")
gate_log = log_DB("Gate_Log")


#path = "E:\\" #Windows
path = " " #Linux

######################################################
#                  Serial Functions                  #
######################################################
#test when scanner not in system
scanner_bypass = True

#Init Serial Comms
def start_scanner():
    COM = "/dev/ttyACM0" #Linux
    #COM = "COM4"          #Windows
    BAUD = 9600
    if not scanner_bypass:
        try:
            global ser
            ser = serial.Serial(COM, BAUD, timeout = 0.00625)
        except:
            print("Scanner Unavailable")
            input()


#Read serial line and write to log
def read_scanner():
    if not scanner_bypass:
        while True:
            val = str(ser.readline().decode('ascii'))
            if len(val) > 4:
                print()
                return val
                break
    else:
        val = input("Scanner Input : ")
        return val

######################################################
#                Relay GPIO Functions                #
######################################################
#Define Pins
pin = 18    # Lock relay
switch = 17 # Lock reed switch

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)

#Pin functions
def relayHigh():
    GPIO.output(pin, GPIO.HIGH)
    
def relayLow():
    GPIO.output(pin, GPIO.LOW)


######################################################
#                 User Menu Functions                #
######################################################

#interfaces with techs DB to add user
def add():
    name=input("Full Name: ")
    login=input("Login: ")
    print("Scan Badge: ")
    badge=read_scanner()
    permissions=input("Permissions: ")    
    print(name," ",login," ",badge," ",permissions)
    print("Correct(Y/N): ",end="")
    state = input()
    if state==("y" or "Y"):
        techs.add(name,login,badge,permissions)
    else:
        add()

#interfaces with techs DB to remove user
def remove():
    print("Scan Badge: ",end="")
    badge=read_scanner()
    techs.remove(badge)

#interfaces with techs DB to check if user is in DB
def check_user():
    print("Scan Badge: ",end="")
    badge=read_scanner()
    if techs.check_user(badge):
        print("Badge:",badge,"    Name:",techs.get_name(badge))
    else:
        print("Badge:",badge," not found.")
    print("Press and key to close.....",end="")
    input()

#interfaces with techs DB to check users permission level
def check_permissions():
    print("Scan Badge: ",end="")
    badge=read_scanner()
    print("Permissions Level:",techs.check_permissions(badge))
    print("Press and key to close.....",end="")
    input()

#interfaces with techs DB to display contents
def dump(db):
    db.dump()
    print("Press and key to close.....",end="")
    input()
    os.system('clear')

#interfaces with techs DB to export to specified path
def export(db,name,path):
    print(str(path)+name+time_output()[0:10])
    db.export(path+name)

#displays menu for admin to use pervious functions
def user_admin_menu():
    print("""
_________________________________
1)Add User
2)Remove User
3)Check For User
4)Check Permissions
5)Display All Users
6)Export to .csv
7)Back to Main Menu
_________________________________
""")
    state=input()
    os.system('clear')
    if state == "1":
        add()
    if state == '2':
        remove()
    if state == '3':
        check_user()
    if state == '4':
        check_permissions()
    if state == '5':
        dump(techs)
    if state == '6':
        export(techs,"techs",path)
    if state == '7':
        main_menu()
    os.system('clear')

######################################################
#                  Main Menu                         #
######################################################
#returns timestamp
def time_output():
	time=int(timestamp())
	output= str(datetime.datetime.fromtimestamp(time).isoformat())
	return output.replace("T"," ")

#interfaces with GPIO to control gate
def open_gate():
    print("Scan Badge...")
    scan = read_scanner()
    #if badge scanned is in the tech DB and has elevated permissions, Open gate and check the time
    if techs.check_user(scan) and techs.check_permissions(scan) < 3:
        print("Gate Open...")
        time_in=time.time()
        relayLow()
        print("Name:",techs.get_name(scan),"Time: ",time_output())
        sleep(5)
        relayHigh()
        while(1):
##            if(GPIO.input(switch)==GPIO.LOW):
##                time_out=time.time()
##                break
            #keyboard feedback instead of Lock's reed switch
            if(input("Press enter when gate is shut")):
                time_out=time.time()
                break
        #when gate is shut check time again to see how long the gate was open 
        time_out=time.time()
        duration = time_out - time_in
        #appends to gate access DB the instance of the gate being opened
        gate_log.add(time_output(), techs.get_name(scan), int(duration))
        
    else:
        print("Insufficient Permissions...")
        input()

#check badge and permissions level to access admin page
def access_admin_menu():
    print("""
_________________________________
1) Badge
2) Keyboard
_________________________________
""")
    state=input()
    os.system('clear')
    if(state == '1'):
        print("Scan Badge...")
        scan = read_scanner()
        if techs.check_user(scan) and techs.check_permissions(scan) < 2:
            user_admin_menu()
        else:
            print("Need Admin Permissions...")
            input()
    elif(state == '2'):
        scan = getpass.getpass("Enter Admin Account...")
        if techs.check_user(scan) and techs.check_permissions(scan) < 2:
            user_admin_menu()
        else:
            print("Need Admin Permissions...")
            input()

#print main menu for users to use functions above
def main_menu():
    print("""
_________________________________
1)Open Gate
2)Edit Users
3)Display Records
4)Export to .csv
5)Restart Scanner
_________________________________
""")
    state=input()
    os.system('clear')
    if state == "1":
        open_gate()
    if state == '2':
        access_admin_menu()
    if state == '3':
        dump(gate_log)
    if state == '4':
        export(gate_log,"Gate_Log",path)
    if state == '5':
        start_scanner()
    os.system('clear')



######################################################
#                   Run Main                         #
######################################################
if __name__=="__main__":
    while True:
        #start serial comms with scanner
        start_scanner()
        #make default admin acount
        techs.add("Admin","Admin","11999","1")
        #lock gate when system is started
        relayHigh()
        #run main menu
        main_menu()




    
