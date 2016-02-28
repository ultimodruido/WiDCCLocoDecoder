################################################################################
# WiDCCLocoDecoder
#
# Created: 2016-02-17 21:50:45.024582
#
################################################################################

from local.WiDCCProtocol import WiDCCProtocol
from local.WiDCCLocoDescriptor import WiDCCLocoDescriptor    
from bcm43362 import bcm43362 as bcm
from wireless import wifi
import socket
import timers
import config



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
        

# everything shoud start from INIT :)
my_state = States.INIT

# create the loco descriptor
my_loco = WiDCCLocoDescriptor.LocoDescriptor()
my_socket = socket.socket()
my_com_timer = timers.timer()
my_config = config.Config()



###########################
# states machine functions
###########################

# INIT: startup decoder and drivers
def f_init():
    print("INIT")
    
    # start wifi driver
    bcm.auto_init()
    
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
        pass
    
    
    # read config.txt file
    # set loco ID
    my_loco.loco_id = my_config.id
    
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

    if wifi.is_linked():
        my_state = States.WIFI_TCP_LINK




# WIFI_CONFIGURE: set up of wifi connection's params
def f_wifi_configure():
    print("WIFI_CONFIGURE")
    

# WIFI_TCP_LINK: any final action needed before operation
def f_wifi_tcp_link():
    print("WIFI_TCP_LINK")
    if not wifi.is_linked():
        my_state = States.WIFI_START
        
    my_socket.connect(my_config.server)

    
# RUNNING: the loco is ready to run
def f_running():
    print("RUNNING")
    if not wifi.is_linked():
        my_state = States.WIFI_START
        
        

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