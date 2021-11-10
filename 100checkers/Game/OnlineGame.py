'''import socket
import threading
import pickle
import struct
from enum import Enum
from Game.GameWindows import Interface as I


class Server:
    def __init__(self):
        self.thread = threading.Thread(target=self.update)
        self.thread.start()
        self.socket = socket.socket()
        self.socket.bind(('localhost', 9090))
        self.socket.listen(1)
        self.socket_client, self.address_client = self.socket.accept()
        self.connection = Connection(self.socket)
        self.data_treatment()

    def data_treatment(self):
        while True:
            self.game = I.game
            data = self.socket_client.recv(1024)
            if not data:
                break
            self.socket_client.send(self.connection.send_object(self.game))


    def update(self):
        commands = {
            Commands.UNDO: self.game.undo_game,
            Commands.REDO: self.game.redo_game,
            Commands.MOTION: self.game.step,
            Commands.SAVE: self.game.save_game,
            Commands.LOAD: self.game.load_game
        }
        obj = self.connection.receive_object()
        #obj = (Commands.MOTION, 1, 2)
        command = obj[0]
        commands[command](*obj[1:])


class Client:
    def __init__(self):
        self.thread = threading.Thread(target=self.send_keywords)
        self.socket = socket.socket()
        self.socket.connect('localhost', 9090)
        self.data = self.socket.recv(1024)

    def send_message(self, message_type ):
        self.socket.send()


class Connection:
    def __init__(self, socket):
        self.socket = socket

    def receive_object(self):
        len_object = struct.unpack('i',self.socket.recv(4))
        obj_bytes = self.socket.recv(len_object)
        return pickle.loads(obj_bytes)

    def send_object(self, obj):
        pickled_obj = pickle.dumps(obj)
        len_p_obj = struct.pack('i', len(pickled_obj))
        self.socket.send(len_p_obj)


class Commands(Enum):
    UNDO = 0
    REDO = 1
    MOTION = 2
    SAVE = 3
    LOAD = 4'''


