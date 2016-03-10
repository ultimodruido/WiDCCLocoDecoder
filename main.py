################################################################################
# WiDCCLocoDecoder
#
# Created: 2016-02-17 21:50:45.024582
#
################################################################################

from local.WiDCCProtocol import WiDCCProtocol
#from local.WiDCCLocoDescriptor import WiDCCLocoDescriptor
from bcm43362 import bcm43362 as bcm
from wireless import wifi#, select
import socket
#import timers
#import config
import threading
#import fifo

# import the global variable shared across modules
from memory_context import *


###########################
# states machine functions
###########################


def f_state_init():
""" ### ### ### ###
# INIT: startup decoder and drivers
# at this step only hw settings like
# digital IN/OUT are performed
# it accesses the global variables so 
# include the following in your file:
# from memory_context include *
### ### ### ### """
    print("STATE INIT")
    
    # start wifi driver
    bcm.auto_init()
    sleep(250)
    
    # set hw platform from config
    # define digital pin IN/OUT
    # TODO
    
    # move to CONFIG
    my_state = States.CONFIG


def f_state_config():
""" ### ### ### ###
# CONFIG: startup software params
# at this step only sw settings like
# loco ID and wifi settings are configured
# it accesses the global variables so 
# include the following in your file:
# from memory_context include *
### ### ### ### """
    print("STATE CONFIG")

    # read config.txt file
    # set loco ID
    if my_config.loco_id:
        my_loco.loco_id = my_config.loco_id
    else:
        my_loco.loco_id = random() #look for embedded random function
    
    # check if connection data are available
    if my_config.wifi_net ==  "WiDCC_config" :
        my_state = States.WIFI_CONFIGURE
    else:
        # move to state "try connect"
        my_state = States.WIFI_START


def f_state_wifi_start():
""" ### ### ### ###
# WIFI START: if wifi connection settings are
# are known then try to connect to the network
# it accesses the global variables so 
# include the following in your file:
# from memory_context include *
### ### ### ### """
    print("STATE WIFI_START")
    
    for retry in range(10):
        try:
            wifi.link(my_config.wifi_net, wifi.WIFI_WPA2, my_config.wifi_pwd)
            
        except Exception as e:
            my_state = States.WIFI_CONFIGURE
            print(e)

    sleep(250)
    if wifi.is_linked():
        my_state = States.WIFI_TCP_LINK


def f_state_wifi_configure():
""" ### ### ### ###
# WIFI_CONFIGURE: if wifi connection settings 
# are unknown then try to connect to a 
# predifined network that allows the storage
# of updated wifi connection params
# it opens a server listening at 87246
# it expect a MessageConfig with the new
# settings. If everything goes right then a 
# new config file is stored in flash memory
# and the state machine is re-set to CONFIG
# it accesses the global variables so 
# include the following in your file:
# from memory_context include *
### ### ### ### """
    print("STATE WIFI_CONFIGURE")
    # connect to the standard wifi to configure
    # wifi settings
    for retry in range(10):
        try:
            wifi.link(my_config.wifi_net, wifi.WIFI_WPA2, my_config.wifi_pwd)
            
        except Exception as e:
            print(e)

    
    if wifi.is_linked():
        test_socket = socket.socket()
        test_socket.bind(('', WiDCCProtocol.SERVER_PORT))
        test_socket.listen(1)
        test_client, _ = accept()
        msg = ''
        while 1:
            data = test_client.recv(64)
            msg += data
            if not data:
                break
        test_client.close()
        test_socket.close()
        try:
            message = WiDCCProtocol.read_message(msg)
            if message.msg_type == "Config":
                my_config.loco_id = message.loco_id
                my_config.wifi_net = message.wifi_net
                my_config.wifi_pwd = message.wifi_pwd
                my_config.save()
                my_state = States.CONFIG            
        except:
            pass         
        wifi.unlink()
        
    else:
        sleep(500)
   

def f_state_wifi_tcp_link():
""" ### ### ### ###
# WIFI_TCP_LINK: if wifi connection is up
# and running, it opens a TCP connection and 
# tries to Login to the WiDCC server.
# A MessageLogin is sent and login is considered 
# successful only if a MessageRegistered is
# received.
# It accesses the global variables so 
# include the following in your file:
# from memory_context include *
### ### ### ### """
    print("STATE WIFI_TCP_LINK")
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



# RUNNING: the loco is ready to run
def f_state_running():
""" ### ### ### ###
# RUNNING: if the loco is registered to the
# server, normal operation can start.
# A recurring function is executed to keep the
# connection alive. Received inputs are being
# processed and eventually feedbacks to the 
# server is added to the transmission list.
# It accesses the global variables so 
# include the following in your file:
# from memory_context include *
### ### ### ### """
    print("STATE RUNNING")
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
def f_state_error():
    print("STATE ERROR")
    #restart and sleep 3s
    my_state = States.INIT
    sleep(3000)
    
    
    
###########################
# mail loop
###########################

while True:
    if my_state == States.INIT:
        f_state_init()
    elif my_state == States.CONFIG:
        f_state_config()
    elif my_state == States.WIFI_START:
        f_state_wifi_start()
    elif my_state == States.WIFI_CONFIGURE:
        f_state_wifi_configure()
    elif my_state == States.WIFI_TCP_LINK:
        f_state_wifi_tcp_link()
    elif my_state == States.RUNNING:
        f_state_running()
    elif my_state == States.ERROR:
        f_state_error()
    else:
        print("unknown state status ->ERROR")
        f_state_error()   
    
    sleep(50)