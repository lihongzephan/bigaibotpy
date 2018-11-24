from time import sleep, time
from decimal import *
import g
import datetime
import traceback
import math
import socket
import threading
import sys
import random
import aiml

alice = aiml.Kernel()
alice.learn("std-startup.xml")
alice.respond('load aiml b')

LOGINID = str(random.randint(1000,9999))
HOST = "localhost"
PORT = 9013


def funQuit():
    pass

def StartProgram():
    #strMenuTitle = 'Socket Client'
    #listMenu = ['Connect Server','Quit']
    #listFunction = ['funConnectServer','funQuit']
    #g.rb.ShowMenu(strMenuTitle, listMenu, listFunction)
    funConnectServer()

def funConnectServer():
    #g.rb.DisplayWholeString("Program Starts")

    global sock, gbolHeartBeat, gbolLogin, LOGINID, client_thread

    # timLastHB is the last time that we receive HeartBeat from the socket server
    global gtimLastHB, gintHBLimit, gbolWorking

    gintHBLimit = 10

    try:
        bolProgramEnd = False

        while not bolProgramEnd:
            # First Time Display is Slow, so display First
            #g.rb.DisplaySingleString(0, 0, "Connecting to Server ...", True)
            #g.rb.DisplaySingleString(0, 15, "Host: " + HOST, False)
            #g.rb.DisplaySingleString(0, 30, "Port: " + str(PORT), False)

            # Connect to server

            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            bolConnectedWithoutTimeout = False
            floConnectTimeStart = time()
            gbolLogin = False
            while not bolConnectedWithoutTimeout:
                try:
                    if time() - floConnectTimeStart > 600:
                        # Try to connect more than 600 seconds, so exit program
                        sys.exit()
                    else:
                        sock.settimeout(10)
                        sock.connect((HOST, PORT))
                        sock.setblocking(1)
                        bolConnectedWithoutTimeout = True
                except:
                    # Here unable to connect server, may be the connection is permanently lost
                    # Exit app, fix connection problem and run client again!!!
                    # sys.exit()
                    bolConnectedWithoutTimeout = False


            # Arrive Here Means Already Connected

            

            # To avoid the EV3 Brick stops at sock.recv (here we use blocking mode),
            # Here we start the sock.recv in another thread
            client_thread = threading.Thread(target=StartClientReceive)
            client_thread.daemon = True
            client_thread.start()



            # Here Send Login ID
            if not gbolLogin:
                strTemp = "|||LOGIN" + LOGINID
                sock.sendall(strTemp.encode())
                sleep(5)



            # Initialize gtimeLastHB
            gtimLastHB = time()

            # Start Sending HeartBeat to server
            gbolHeartBeat = True
            funHBStart()

            bolEnd = False
 
            while not bolEnd:
            # Start while not bolEnd
                # Check if socket disconnected
                if time() - gtimLastHB > gintHBLimit:
                    gbolHeartBeat = False

                    # First Time Display is Slow, so display First
                    #g.rb.DisplaySingleString(0, 0, "No HeartBeat received", True)
                    #g.rb.DisplaySingleString(0, 15, "Reconnnect Later", False)

                    sock.shutdown(socket.SHUT_RDWR)
                    sock.close()

                    sleep(3)

                    bolEnd = True
                    gbolHeartBeat = False
                    gbolLogin = False
                    try:
                        client_thread.stop()
                    except:
                        pass
                    # Try to stop all motors
                    #try:
                        #g.rb.StopRobot(g.mtp)
                    #except:
                        #pass

                # Check for keypress and exit program
                #if g.rb.btn.any():
                    # If Any Button is pressed, Exit Program
                    # Try to stop all motors
                    #try:
                        #g.rb.StopRobot(g.mtp)
                    #except:
                        #pass
                    #gbolHeartBeat = False
                    #gbolEnd = True
                    #bolProgramEnd = True
                    #try:
                       #client_thread.stop()
                    #except:
                       #pass

                # Sleep for a while
                sleep(0.05)
            # End while not bolEnd
        #End while not bolProgramEnd
    #End try
    finally:
        # Try to stop all motors
        #try:
            #g.rb.StopRobot(g.mtp)
        #except:
            #pass
        StartProgram()
#End funConnectServer


# Start HeartBeat
def funHBStart():
    thrHB = threading.Timer(2, funHeartBeat)
    thrHB.start()

def funHeartBeat():
    global sock, gbolHeartBeat
    try:
        sock.sendall("HBHBHBHB".encode())
        #g.rb.DisplaySingleString(0, 0, "HeatBeat Sent", True)
    except:
        #g.rb.DisplaySingleString(0, 0, "Send HB Failed", True)
        pass

    if gbolHeartBeat:
        funHBStart()



# Function to receive data from Socket Server, this function is to be started in another thread
def StartClientReceive():
    global sock, gintTotalCommand, glstCommand, bolReConnect, gtimLastHB, LOGINID

    bolEnd = False

    while not bolEnd:
        # Receive Data From Server and store it inside the list glstCommand
        received = str(sock.recv(1024).decode('utf-8'))

        # g.rb.DisplayWholeString("Received: " + received)
        
        if received == "":
            # Socket disconnected, may be due to mobile phone connection lost
            # There are 2 situations to determine whether the connection is lost
            # 1. received = ""
            # 2. We need to use the heartbit technique, if there is no response from the socket server for a particular time, say 5 seconds, then the connectio is assumed to be lost
            # The following codes deal with situation 1
            bolEnd = True
            bolReConnect = True
        elif received == "|LOGINOK":
            # Display Login Successful
            gbolLogin = True
            #g.rb.DisplayWholeString("Login Successful: " + LOGINID)
        elif received == "HBHBHBHB":
            # Got HeartBeat from socket server, reset gtimLastHB
            gtimLastHB = time()
        elif received == "STOPROBOT":
            pass
            # Try to stop all motors
            #try:
                #g.rb.StopRobot(g.mtp)
            #except:
                #pass
        elif received[0:8] == "MESSAGE:":
            # Message from Socket.IO Server
            strTemp = received[8:]
            try:
                #g.rb.DisplayWholeString("intLeft: " + str(intLeft) + "   intRight: " + str(intRight))
                #g.rb.MoveRobot(g.mtp, "F", intLeft, intRight, 0, True)
                strAnswer = 'ANSWER::' + alice.respond(strTemp)
                sock.sendall(strAnswer.encode())
            except:
                pass
        else:
            # Normal Receive
            #gintTotalCommand += 1
            #glstCommand.append(received)

            if received == "||Disconnect":
                bolEnd = True
        #End if received == ""
#End StartClientReceive
