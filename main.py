################################################################################
# WiDCCLocoDecoder
#
# Created: 2016-02-17 21:50:45.024582
#
################################################################################

from local.WiDCCProtocol import WiDCCProtocol
from local.WiDCCLocoDescriptor import WiDCCLocoDescriptor
from drivers.wifi.bcm43362 import bcm43362 as bcm
from wireless import wifi
from enum import Enum


# set up state machine
States = Enum('States', 'INIT CONFIG WIFI_START  WIFI_CONFIGURE WIFI_TCP_LINK RUNNING ERROR')

# everything shoud start from INIT :)
my_state = States.INIT

# create the loco descriptor
my_loco = WiDCCLocoDescriptor.LocoDescriptor()

if my_state = States.INIT:
    f_init()
elif my_state = States.CONFIG:
    f_config()
elif my_state = States.WIFI_START:
    f_wifi_start()
elif my_state = States.WIFI_CONFIGURE:
    f_wifi_configure()
elif my_state = States.WIFI_TCP_LINK:
    f_wifi_tcp_link()
elif my_state = States.RUNNING:
    f_running()
elif my_state = States.ERROR:
    f_error()


###########################
# states machine functions
###########################

# INIT: startup decoder and drivers
def f_init():
    
    # start wifi driver
    bcm.auto_init()
    
    # move to CONFIG
    my_state = States.CONFIG



# CONFIG: configure the decoder
def f_config():

    # check if config.txt exists
    try:
        with open('spamspam.txt', 'w', opener=opener) as f
    except:
        # create the first config
        pass
    
    
    # read config.txt file
    # import from file
    
    # check if connection data are available
    if my_config.wifi_net ==  None:
        my_state = States.WIFI_CONFIGURE
    else:
        # move to state "try connect"
        my_state = States.WIFI_START



# WIFI_START: connect to network
def f_wifi_start():
    pass
    
# WIFI_CONFIGURE: set up of wifi connection's params
def f_wifi_configure():
    pass

# WIFI_TCP_LINK: any final action needed before operation
def f_wifi_tcp_link():
    pass
    
# RUNNING: the loco is ready to run
def f_running():
    pass

# ERROR: special state where the loco informs about problems
#        with special blinking patterns
def f_error():
    pass