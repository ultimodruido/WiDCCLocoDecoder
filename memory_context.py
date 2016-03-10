
from local.WiDCCLocoDescriptor import WiDCCLocoDescriptor    
from socket import socket
from timers import timer
from config import Config
from fifo import Fifo
from threading import Lock

# set up state machine
class States():
    def __init__(self):
        self.INIT = 1
        self.CONFIG = 2
        self.WIFI_START = 3
        self.WIFI_CONFIGURE = 4
        self.WIFI_TCP_LINK = 5
        self.RUNNING = 6
        self.ERROR = 7
        

# everything should start from INIT :)
my_state = States.INIT

# creating the global variables
my_loco = WiDCCLocoDescriptor.LocoDescriptor()
my_socket = socket()
my_socket.setblocking(False)
my_socket_lock = Lock()
my_com_timer = timer()
my_com_timer_counter = 0
my_config = Config()
msg_queue_in = Fifo(4)
msg_queue_out = Fifo(2)
msg_queue_in_lock = Lock()
msg_queue_out_lock = Lock()

