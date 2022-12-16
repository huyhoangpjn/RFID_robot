import serial
import time
import sys

def connect_and_run():
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM16'
    ser.timeout = None
    try:
        ser.open()
    except:
        print("Can't connect to the robot...")
    return ser

def get_data(ser):
    while True:
        data = ser.readline()
        with open("incomming_data.txt", 'w') as f:
            f.write(data.decode('utf-8'))
            f.close()
        

ser = connect_and_run()
get_data(ser)