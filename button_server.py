import socket
from threading import Thread
import os
import time
import selectors


class Server():
    clients = {}
    button_status = ""
    round_over = False
    start = False

    sel = selectors.DefaultSelector() 

    def __init__(self, HOST, PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((HOST, PORT))
        self.socket.listen()
        print(f"Waiting for connections...")

    #Listen for new clients to join server and handle clients in their own threads
    def listen(self):
        Thread(target=self.listen_for_start).start()
        while True:
            client_socket, address = self.socket.accept()
            data = {'addr': address, 'messages' : []}
            Server.sel.register(client_socket, selectors.EVENT_READ, data=data)
            print(f"Connection made with {address}")
            Thread(target=self.handle_new_client,args=(client_socket,)).start()

    
    #When at least 2 players, listen for input to start round. This is handled in a thread in case new users want to join while the game is ongoing
    #Will then start the main game loop -> Therefore in same thread
    def listen_for_start(self):
        done = False
        while not done:
            if len(Server.clients) >= 2:
                if input("Type Y to start the round") == "Y":
                    done = True
        self.broadcast_message("start")
        self.main_loop()

    #Get client name and add to client dictionary
    def handle_new_client(self, client_socket):
        client_name = client_socket.recv(1024).decode()
        Server.clients.setdefault(client_socket, client_name)

    #Message handling when event is detected by selector
    #Will broadcast winning player and declare the round as over
    def callback(self,key, mask):
        client_socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            recv_data = client_socket.recv(1024).decode()
            if recv_data and recv_data != "q":
                Server.round_over = True
                self.broadcast_message(Server.clients[client_socket] + " has pushed the button first! Round is over.")
            else:
                Server.sel.unregister(client_socket)

    #Broardcast encoded string to clients
    def broadcast_message(self, message):
        for client in Server.clients:
            client.send(message.encode())

                    
    #Main game loop
    def main_loop(self):
        done = False 
        while not done:
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            time.sleep(1)
            print("GO")

            #Event detection to detect the first client to send a message during periods when round_over = False
            events = Server.sel.select(timeout=10)   #Round will proceed for 10 seconds without an event before declaring the round as over
            for key, mask in events:
                if key.data:
                    self.callback(key, mask)

            if Server.round_over == True:
                self.broadcast_message("round_over")
                Server.round_over = False
                if input("Would you like to do another round? (Y/N)") == "Y":
                    self.broadcast_message("start")
                    continue
                else:
                    done = True
        self.broadcast_message("quit")
        self.socket.close()
        Server.sel.close()
        os._exit(0)    

if __name__ == "__main__":
    server = Server("127.0.0.1",5000)
    server.listen()

        

        
