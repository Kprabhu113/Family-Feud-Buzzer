import socket
from threading import Thread
import os

class client():

    round_over = False

    def __init__(self, HOST, PORT):
        self.name = input("Enter a name: ")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST,PORT))

        self.talk_to_server()

    #Initialize threading to receive messages and send client name to server
    def talk_to_server(self):
        self.socket.send(self.name.encode())
        Thread(target=self.receive_message).start()
        self.send_message()

    #Sending message to server (button press) only when a round is ongoing
    def send_message(self):
        while True:
            message = input("")
            if message == "q":
                self.kill_self()
            else:
                if client.round_over == False:
                    self.socket.send(message.encode())

    #Receive server broadcasts to announce state of the game
    def receive_message(self):
        while True:
            message = self.socket.recv(1024).decode()
            if message == "round_over":
                client.round_over = True
            elif message == "start":
                client.round_over = False
            elif message == "quit":
                self.kill_self()
            else:
                print("\033[1;31;40m" + message + "\033[0m")

    #Cleanup
    def kill_self(self):
        self.socket.close()
        os._exit(0)

        
if __name__ == "__main__":
    client("127.0.0.1",5000)

