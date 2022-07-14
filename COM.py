import serial
import subprocess

class MySerial:
    def __init__(self):
        p = subprocess.check_output("python -m serial.tools.list_ports")
        ports = p.replace("\n", " ").split()
        for i in range(len(ports)):
            print("port " + str(i) + " : " + ports[i])

        port_n = input('Input port number: ')
        print("Your select : " + str(ports[int(port_n)]))
        self.port = ports[int(port_n)]
        self.ser = serial.Serial(
            port=self.port,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=None)


    def open(self):
        if self.ser.isOpen():
            pass
        elif not self.ser.isOpen():
            self.ser.open()


    def close(self):
        self.ser.close()


    def read(self):
        self.open()

        while True:
            result = ''
            while self.ser.inWaiting() == 0:
                pass
            result = self.ser.readline()
            if result != None:
                return result


    def write(self, data):
        try:
            self.ser.open()
        except:
            pass
        try:
            self.ser.write(data)
        except:
            return(False)
        self.ser.close()
        return(True)


'''
while ser.inWaiting() == 0:
    pass
#необходимая работа с данными...'''


class MyDevises:
    def __init__(self, name, type):
        self.name = name
        self.serial = MySerial()
        self.type = type

    def testing(self):
        self.serial.write('test')

    def turn_on(self):
        pass

    def turn_off(self):
        pass