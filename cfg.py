import json

class Config():
    def __init__(self):
        # first check the existance of a stored file
        stored_dict = None
        try:
            f = open("/storage/extSdCard/config.txt", "r")
            try:
                stored_dict = json.load(f)#f.read()
            except:
                stored_dict = self.load_defaults()
            finally:
                f.close()
        except:
            stored_dict = self.load_defaults()
            
        # set params value
        #print("stored_dict")
        #print( stored_dict )
        self.loco_id = stored_dict['loco_id']
        self.wifi_net = stored_dict['wifi_net']
        self.wifi_pwd = stored_dict['wifi_pwd']
        
    #def __setattr__(self, name, value)
    
    def save(self):
        f = open("/storage/extSdCard/config.txt", "w")
        json.dump(self.__dict__, f)
        f.close()
        
    def load_defaults(self):

        data = dict( loco_id = None,
            wifi_net = "WiDCC_config",
            wifi_pwd = "Cnfig_87246" )
        return data
        
    def pin_cfg_photon_test(loco):
        """ ### ### ### ###
        # sets the pin configuration for the test
        # hw basen on the particle photon.
        # takes the loco descriptor and stores the
        # hw pins setup of the following features:
        # 1 - motor control
        # 2 - direction
        # 3 - light front
        # 4 - light rear
        # no extra functions are considered
        ### ### ### ### """
        try:               
            loco.pins.motor = D12
            loco.pins.direction = D7
            loco.pins.light_front = D13
            loco.pins.light_rear = D14
        
            # set the pins as digital output
            # TODO
            pinMode( loco.pins.motor = OUTPUT )
            pinMode( loco.pins.direction = OUTPUT )
            pinMode( loco.pins.light_front = OUTPUT )
            pinMode( loco.pins.light_rear = OUTPUT )
            
        except:
            raise PinSetupError



# exceptions definition    
new_exception(Error, Exception, "Error in Config()")     
new_exception(PinSetupError, Error, "Error configuring HW pins") 