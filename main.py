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


# INIT: startup decoder and drivers
# start wifi driver
bcm.auto_init()

my_loco = WiDCCLocoDescriptor.LocoDescriptor()

# CONFIG: configure the decoder
#read config.txt file




# WIFI_INIT: connect to network

