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
        
    
        