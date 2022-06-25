import socket
import time

HOST = "192.168.43.121"
PORT = 65432
id=100

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn,addr = s.accept()
    id= id+1
    with conn :
        start = time.time()
        data = conn.recv(1024)
        data = data.decode('utf-8')
        #print(F"Received{data!r}")
        print("Drone id : ",id, " and Latitude of Drone : ", data,"\n")
        lt = data.split()
        print(float(lt[2]),"\n")
        lat_min = float(lt[2])
        data1 = conn.recv(1024)
        data1 = data1.decode('utf-8')
        #print(F"Received{data1!r}")


        print("Drone id : ",id, "and Longitude of Drone : ", data1,"\n")
        ln = data1.split()
        print(float(ln[2]),"\n")
        long_min = float(ln[2])


        if lat_min>= 0.7100 and lat_min<=0.79999 and long_min>=20.4000 and long_min<=20.8000:   
        #if data == "26 deg 00.7425 min" and data1=="076 deg 20.7050 min":
            print("Drone is in security sensitive area \n")
            print("Controller sending RTL Execution Command\n")
            conn.sendall(b"RTL")
            data2 = conn.recv(1024)
            data2 = data2.decode('utf-8')
            print("Received acknowledgement from Drone", data2,"\n")
            #print(F"Received{data!r}")
            end= time.time()
            #print(end - start)
        
            #else :
            #    print("Not reached to boundary conditions")
			#conn.sendall(data)



