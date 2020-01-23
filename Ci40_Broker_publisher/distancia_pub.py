import socket
import time
import os

PORT = 3000
IP_BROKER = "192.168.1.92"
TOPIC = "distancia"
IP_SERVER = "::"

server_socket = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
server_socket.bind((IP_SERVER, PORT))
print("Servidor escuchando...")

while True:
    message, address = server_socket.recvfrom(1024)
    message = message.decode()
    print("Datos recibido: ",message)
    if message is not None or message != "":
    	command = "mosquitto_pub -h " + IP_BROKER + " -t '" + TOPIC + "' -m '" + message + "'" 
    	os.system(command)
    	print(command)





    