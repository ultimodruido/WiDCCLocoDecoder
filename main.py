################################################################################
# WiDCCLocoDecoder
#
# Created: 2016-02-17 21:50:45.024582
#
################################################################################

from local.WiDCCProtocol import WiDCCProtocol
from local.WiDCCLocoDescriptor import WiDCCLocoDescriptor    
from bcm43362 import bcm43362 as bcm
from wireless import wifi#, select
import socket
import timers
import config
import threading
import fifo

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
#socket_list = List()
#socket_list.append(my_socket)
my_com_timer = timers.timer()
my_com_timer_counter = 0
my_config = config.Config()
msg_queue_in = fifo.Fifo(4)
msg_queue_out = fifo.Fifo(2)
msg_queue_in_lock = threading.Lock()
msg_queue_out_lock = threading.Lock()


###########################
# states machine functions
###########################

# INIT: startup decoder and drivers
def f_init():
    print("INIT")
    
    # start wifi driver
    bcm.auto_init()
    sleep(250)
    
    # move to CONFIG
    my_state = States.CONFIG



# CONFIG: configure the decoder
def f_config():
    print("CONFIG")
    # check if config.txt exists
    try:
        print("open config file")
        #with open('spamspam.txt', 'w', opener=opener) as f
    except:
        # create the first config
        my_state = States.WIFI_CONFIGURE
        return
    
    
    # read config.txt file
    # set loco ID
    if my_config.id:
        my_loco.loco_id = my_config.id
    else:
        my_loco.loco_id = random() #look for embedded random function
    
    # check if connection data are available
    if my_config.net ==  None:
        my_state = States.WIFI_CONFIGURE
    else:
        # move to state "try connect"
        my_state = States.WIFI_START



# WIFI_START: connect to network
def f_wifi_start():
    print("WIFI_START")
    
    for retry in range(10):
        try:
            wifi.link(my_config.net, wifi.WIFI_WPA2, my_config.pwd)
            
        except Exception as e:
            my_state = States.WIFI_CONFIGURE
            print(e)

    sleep(250)
    if wifi.is_linked():
        my_state = States.WIFI_TCP_LINK




# WIFI_CONFIGURE: set up of wifi connection's params
def f_wifi_configure():
    print("WIFI_CONFIGURE")
    # understand how to create a soft AP
    

# read and send helper functions for transmitting 
# data over TCP
def f_tcp_send_msg(msg):
    # transmit a full message over TCP
    # it checks if the message is fully 
    # transmitted, if not reiterates
    msg_len = len(msg)
    sent_len = 0
    while sent_len < msg_len:
        buf_len = my_socket.send(msg[sent_len:])
        sent_len += buf_len

def f_tcp_feedback_msg():
    # waits for the server reply - blocking!!!
    
    data = my_socket.recv(128)
    sent_len = len(data)
    while sent_len:
        buf = my_socket.recv(128)
        data += buf
        sent_len = len(buf)
         
    return data

# function to be threaded that handle communication
# over tcp
def f_tcp_communication():
    print("tcp_communication start")
    
    # do I need lock on the socket to prevent
    # simultaneous connections attempt?
    my_socket_lock.acquire()
    print("tcp_communication lock acquired")
    my_socket.connect(my_config.server)
    if msg_queue_out.isEmpty():
        # send messageAlive
        msg = WiDCCProtocol.create_message(my_loco, "Alive")          
        f_tcp_send_msg(msg)
    else:
        # create a for loop with 
        # send msg_queue_out.get():
        # sending max 2 messages
        # not sure if it works...
        # may be better to stick to
        # only 1 message x connection
        # it is easier to handle
        # need to check if the in buffer
        # gets full...
        msg_queue_out_lock.acquire()
        msg = WiDCCProtocol.create_message(my_loco, msg_queue_out.get() )
        msg_queue_out_lock.release()    
        f_tcp_send_msg(msg)
    my_socket_lock.release()

    # every 3 transmission automtically send a
    # Status message    
    if my_com_timer_counter >= 3:
        my_com_timer_counter = 0
        msg_queue_out_lock.acquire()
        msg_queue_out.insert("Status")
        msg_queue_out_lock.release()
    
    my_com_timer_counter += 1
            
    # wait for the reply
    msg = f_tcp_feedback_msg()
    message = WiDCCProtocol.read_message(msg)
    if not message.msg_type == "ACK":
        msg_queue_in_lock.acquire()
        msg_queue_in.put(message)
        msg_queue_in_lock.release()
        
    print("tcp_communication end")        
        

# WIFI_TCP_LINK: any final action needed before operation
def f_wifi_tcp_link():
    print("WIFI_TCP_LINK")
    if not wifi.is_linked():
        my_state = States.WIFI_START
        return 
    try:    
        my_socket.connect(my_config.server)
        
        # register our decoder to the server
        msg = WiDCCProtocol.create_message(my_loco, "Login")
        f_tcp_send_msg(msg)
        
        # wait for feedback
        msg = f_tcp_feedback_msg()
        
        my_socket.close()
        
        message = WiDCCProtocol.read_message(msg)
        
        if message.type == 'Registered':
            my_com_timer.interval( WiDCCProtocol.MSG_PERIOD, f_tcp_communication)
            my_com_timer_counter = 0
               
            # if no error raised, move to running
            my_state = States.RUNNING
    except:
        print("error by tcp link")


# read and implement incoming messages
def f_run_read_msg():
    # once this function is reached better to clear 
    # the message_in list to prevent overflow and to 
    # execute the latest command in case 2 different 
    # commands have been submitted in a row
    print("run_read_message: %s unread", msg_queue_in.elements() )
    while not msg_queue_in.isEmpty():
        msg = msg_queue_in.get()
        print(msg.msg_type)
  
def f_run_prepare_msg():
    # space holder in case here something needs
    # to be done
    pass
  
def f_update_loco_status():
    # updates the status variable of the loco
    # any PID control to slowly adjust the speed
    # is not included here.
    
    # read variables in the my_loco a set/clear
    # the pins
    pass
  
# RUNNING: the loco is ready to run
def f_running():
    print("RUNNING")
    if not wifi.is_linked():
        my_state = States.WIFI_START
        

    # stop the timer if the tcp connection is broken
    # useless if a new connection is started everytime?
    """_, _, err_list = select( [], [], socket_list, timeout = 0 )
    if err_list:
        my_com_timer.clear()        
        my_state = States.WIFI_TCP_LINK
    """
    # check incoming messages
    # do what has to be done
    f_run_read_msg()
    
    # after reading the messages updates
    # to be done once per cycle at least
    f_update_loco_status()
    
    # add eventually new message to send
    f_run_prepare_msg()

# ERROR: special state where the loco informs about problems
#        with special blinking patterns
def f_error():
    print("ERROR")
    
    
    
###########################
# mail loop
###########################

while True:
    if my_state == States.INIT:
        f_init()
    elif my_state == States.CONFIG:
        f_config()
    elif my_state == States.WIFI_START:
        f_wifi_start()
    elif my_state == States.WIFI_CONFIGURE:
        f_wifi_configure()
    elif my_state == States.WIFI_TCP_LINK:
        f_wifi_tcp_link()
    elif my_state == States.RUNNING:
        f_running()
    elif my_state == States.ERROR:
        f_error()
    else:
        pass
    
    sleep(50)