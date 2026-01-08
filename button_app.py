from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from time import sleep

app = Flask(__name__)
app.config['SECRET_KEY'] = "password"

socketio = SocketIO(app)

users = {}

families = []

MAX_PLAYERS = 2

#Check if valid player count
def check_player_num():
    num_players = len(users)
    if num_players < MAX_PLAYERS:
        emit("message", "Waiting for players...", room='server')
        emit("hold", True, broadcast=True)
    else:
        emit("hold",False,broadcast=True)
        emit("message","Press start for another round", room='server')

def reset():
    emit("message","Press start for another round", room='server')
    emit('reset', broadcast = True)

#Start game/round
@socketio.on('start')
def start():
    emit("hold", False, room='client')
    emit("message", "Game started", room='client')
    emit("message", "Question", room='server')

#Load correct html page for server or client
@app.route('/')
def index():
    address = request.remote_addr
    
    if address == "127.0.0.1":
        return render_template("server_index.html")
    else:
        return render_template("client_index.html")

#Handle new client
#Room name (server or client) is passed from connecting device
@socketio.on('join')
def handle_client(data):
    print(data['socket'].handshake.address)
    try:
        room = data['room'] 
        join_room(room)
    except KeyError as msg:
        print("No room given")
        print(msg)
    if room == 'client':
        users[request.sid] = data['username']
        print(users)
        emit("message", f"{data['username']} has joined the game", room='client')
        sleep(2)
    check_player_num()

#Client page button press
@socketio.on("button_pressed")
def handle_message(button):
    if button == "big_button":
        emit("hold", True, room='client')
        emit("message", f"{users[request.sid]} pressed the button first!", broadcast=True)
        sleep(2)
        emit("message","Press start for another round", room='server')
        reset()

#Handle client disconnect
@socketio.on("disconnect")
def handle_disconnect(sid):
    sid = request.sid
    username = users.get(sid, "Anonymous")
    emit("message", f"{username}: has left the game", room='client')
    check_player_num()
    
@socketio.on('addFamily')
def handle_family(family_name):
    families.append(family_name)
    print(families)

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)