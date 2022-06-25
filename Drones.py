from dronekit import connect, VehicleMode
import sys
import time
from pymavlink import mavutil
import socket
import serial
from time import sleep


port = "/dev/ttyUSB0"


HOST = "192.168.43.121"
PORT1 = 65432

# Connect to the Vehicle (in this case a UDP endpoint)
#vehicle = connect('127.0.0.1:14550', wait_ready=True)
vehicle = connect('/dev/ttyACM0', wait_ready=True, baud=57600)
vehicle.mode    = VehicleMode("GUIDED")
vehicle.armed   = True
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST,PORT1))



def decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"


def parseGPS(data):
    try:
	    data = data.decode('utf-8')
    except:
	    print("Cant Parse")
	    return
    #print "raw:", data #prints raw data
    if data[0:6] == "$GPRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print ("no satellite data available")
            return
        print ("---Parsing GPRMC---")
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decode(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = sdata[7]       #Speed in knots
        trCourse = sdata[8]    #True course
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]#date
        location = bytes(lat, 'utf-8')
        s.sendall(location)
        location2 = bytes(lon, 'utf-8')
        s.sendall(location2)
        d1 = s.recv(1024)
        d1 = d1.decode('utf-8')
        if d1 == "RTL" :
            print("Drone is in Security Sensitive Area\n")
            vehicle.mode    = VehicleMode("RTL")
            print("Command recived from Drone network controller, RTL Executed\n")
            s.sendall(b"RTL Executed")
            sleep(2)   
            print("Execution Done")
            print("latitude : ",location,"\n")
            print("longitude : ",location2,"\n")
            exit()
            


while True:
    #print("Global alt Location: %s" % vehicle.location.global_frame.alt)
    data = ser.readline()
    parseGPS(data)
    
        #s.sendall(b"Hello, World")
        

    



