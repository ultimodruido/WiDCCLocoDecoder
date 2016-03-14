################################################################################
# WiDCCLocoDescriptor
#
# Created: 2016-02-07 21:52:49.093460
#
################################################################################

# this is the main library module, add code here

class LocoDescriptor():
    def __init__(self):
        self.loco_id = None
        self.hardware = { 'platform': None ,
                     'firmware': None }
        self.real_speed = 0
        self.target_speed = 0
        self.direction = True
        self.light_auto = False
        self._light_front = False
        self._light_rear = False

        self.F1 = False
        self.F2 = False
        self.F3 = False
        self.F4 = False
        
        #self.wifi_config = { 'net': None ,
        #                    'pwd' : None }
                        
        self.pins.motor = None
        self.pins.light_front = None
        self.pins.light_rear = None
        self.pins.F1 = None
        self.pins.F2 = None
        self.pins.F3 = None
        self.pins.F4 = None
        


    @property
    def light_front(self):
        if self.light_auto:
            if self.direction:
                return True
            else:
                return False
        else:
            return self._light_front
            
    @light_front.setter
    def light_front(self, value):
        self._light_front = value
        
    @property
    def light_rear(self):
        if self.light_auto:
            if self.direction:
                return False
            else:
                return True
        else:
            return self._light_rear
            
    @light_rear.setter
    def light_rear(self, value):
        self._light_rear = value