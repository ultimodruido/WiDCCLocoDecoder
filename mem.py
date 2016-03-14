
from local.WiDCCLocoDescriptor import WiDCCLocoDescriptor    
import socket
import timers
import cfg
import fifo
import threading

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
my_socket = socket.socket()
my_socket.setblocking(False)
my_socket_lock = threading.Lock()
my_com_timer = timers.timer()
my_com_timer_counter = 0
my_config = cfg.Config()
msg_queue_in = fifo.Fifo(4)
msg_queue_out = fifo.Fifo(2)
msg_queue_in_lock = threading.Lock()
msg_queue_out_lock = threading.Lock()

