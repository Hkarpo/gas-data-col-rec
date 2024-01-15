import serial
import time

portName = "/dev/tty.usbmodem143101"                     # replace this port name by yours!
baudrate = 115200
ser = serial.Serial(portName, baudrate)

e1 = b"1"
e0 = b"0"

start_time = time.time()
stop_wtime = time.time()

while stop_wtime - start_time <= 20:
    str = ser.readline()
    # with open('test.txt', 'w') as f:
        # f.write(str)
    print(str)
    if stop_wtime - start_time <= 2:
        ser.write("0".encode())
        print("??????")
    else:
        ser.write("1".encode())
    stop_wtime = time.time()
