import serial
import time

ser = serial.Serial( port="COM6", 
        baudrate=9600, 
        bytesize=8, 
        timeout=1,
        stopbits=serial.STOPBITS_ONE )

print(ser)
time.sleep(2)

# print("wdwe")

ser.write("P|0400".encode('Ascii'))

ser.close()