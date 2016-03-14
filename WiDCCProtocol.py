################################################################################
# WiDCC protocol
#
# Created: 2016-02-04 17:45:07.398596
#
################################################################################
#
# Class collection representing possible messages that can be transferred with
# WiDCC protocol. Serilize and deserialize function for transmission in "plain
# text" form are also provided.
#
# Do not instanziate any Message class directely, use the provided functions
#
# Available functions:
#     read_message(json_txt):
#         input: 
#             - json data
#         returns: 
#             - the Message class corresponding
#         errors: 
#             - WrongMessageType
#             - WrongJsonData
#
#     create_message(loco, msg_type):
#         inputs: 
#             - "loco"
#             - "msg_type"
#         returns:
#             - a Message class of the type spedified in the msg_type
#         errors:
#             - WrongLocoDescriptor
#             - WrongMessageType
#
# Available message types:
#         Login: 
#         Registered:
#         Config:
#         Alive: 
#         Status:
#         Command:
#         Emergency:
#
# Available exceptions:
#         Error: base class from which all exceptions have been derived
#                grab this to get all Exeptions this library raises
#         WrongMessageType: requested message type is not available
#         WrongLocoDescriptor: loco parameter is not a LocoDescriptor instance
#         WrongJsonData: unable to read JSON data
#
#

# let's start with library import
import json
from local.WiDCCLocoDescriptor import WiDCCLocoDescriptor


# container for all registered message types
registry = {}


def _register_class(target_class):
    """register target_class to enable auto deserializion
    This class is reserved and shoudl only be used by the RegisterMeta class"""
    registry[target_class.__name__] = target_class


def read_message(json_txt):
    params = json.loads(json_txt)
    name = params['class']
    target_class = registry[name]
    return target_class(*params['args'])


def create_message(loco, msg_type):
    if not  isinstance(loco, WiDCCLocoDescriptor.LocoDescriptor):
        raise WrongLocoDescriptor
    if not ("Message"+msg_type) in registry:
        raise WrongMessageType

    if msg_type == 'Login':
        return MessageLogin(
            loco.loco_id, 
            loco.hardware['platform'], 
            loco.hardware['firmware']
        )
    elif msg_type == 'Registered':
        return MessageRegistered()
    elif msg_type == 'Config':
        return MessageConfig()
    elif msg_type == 'Alive':
        return MessageAlive(
            loco.loco_id, 
            loco.real_speed, 
            loco.target_speed,
            loco.direction
        )
    elif msg_type == 'Status':
        return MessageStatus(
            loco.loco_id, 
            loco.real_speed, 
            loco.target_speed,
            loco.direction, 
            loco.F1, 
            loco.F2, 
            loco.F3, 
            loco.F4
        )
    elif msg_type == 'Command':
        return MessageCommand(
            loco.loco_id, 
            loco.target_speed,
            loco.direction, 
            loco.F1, 
            loco.F2, 
            loco.F3, 
            loco.F4
        )
    elif msg_type == 'Emergency':
        return MessageEmergency()


class RegisterMeta(type):
    """Meta class that makes automatic the registration of a class for later
    deserializion"""
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        _register_class(cls)
        return cls


class BaseMessage(metaclass = RegisterMeta):
    def __init__(self, *args):
        self.args = args

    def to_json(self):
        return json.dumps({
            'class': self.__class__.__name__,
            'args': self.args
        })


class MessageLogin(BaseMessage):
    def __init__(self, loco_id, decoder_hardware_version, decoder_software_version):
        BaseMessage().__init__(loco_id, decoder_hardware_version, decoder_software_version)
        self.msg_type = 'Login'
        self.loco_id = loco_id
        self.decoder_hardware_version = decoder_hardware_version
        self.decoder_software_version = decoder_software_version


class MessageRegistered(BaseMessage):
    def __init__(self):
        BaseMessage().__init__()
        self.msg_type = 'Registered'
        
        
class MessageNotRegistered(BaseMessage):
    def __init__(self):
        BaseMessage().__init__()
        self.msg_type = 'NotRegistered'


class MessageACK(BaseMessage):
    def __init__(self):
        BaseMessage().__init__()
        self.msg_type = 'ACK'


class MessageConfig(BaseMessage):
    def __init__(self):
        BaseMessage().__init__()
        self.msg_type = 'Emergency'


class MessageAlive(BaseMessage):
    def __init__(self, loco_id, loco_real_speed, loco_target_speed, loco_direction):
        BaseMessage().__init__(loco_id, loco_real_speed, loco_target_speed, loco_direction)
        self.msg_type = 'Alive'
        self.loco_id = loco_id
        self.loco_real_speed = loco_real_speed
        self.loco_target_speed = loco_target_speed
        self.loco_direction = loco_direction


class MessageStatus(BaseMessage):
    def __init__(self, loco_id, loco_real_speed, loco_target_speed, 
                 loco_direction, F1, F2, F3, F4):
        BaseMessage().__init__(loco_id, loco_real_speed, loco_target_speed,
                               loco_direction, F1, F2, F3, F4)
        self.msg_type = 'Status'
        self.loco_id = loco_id
        self.loco_real_speed = loco_real_speed
        self.loco_target_speed = loco_target_speed
        self.loco_direction = loco_direction
        self.F1 = F1
        self.F2 = F2
        self.F3 = F3
        self.F4 = F4


class MessageCommand(BaseMessage):
    def __init__(self,loco_target_speed, loco_direction, F1, F2, F3, F4):
        BaseMessage().__init__(loco_target_speed, loco_direction, F1, F2, F3, F4)
        self.msg_type = 'Command'
        self.loco_target_speed = loco_target_speed
        self.loco_direction = loco_direction
        self.F1 = F1
        self.F2 = F2
        self.F3 = F3
        self.F4 = F4


class MessageEmergency(BaseMessage):
    def __init__(self):
        BaseMessage().__init__()
        self.msg_type = 'Emergency'


class MessageIdentify(BaseMessage):
    def __init__(self):
        BaseMessage().__init__()
        self.msg_type = 'Identify'


class MessageWiFiConfig(BaseMessage):
    def __init__(self):
        BaseMessage().__init__()
        self.msg_type = 'WiFiConfig'
        #add parameters
        
        


# TODO: make it generic to be used also for the server
# same as: class Error(Exception):
new_exception(Error, Exception, "Error in WiDCCProtocol")

# same as: class WrongMessageType(Error):
new_exception(WrongMessageType, Error, "Message type is unknown")

# same as: class WrongLocoDescriptor(Error):
new_exception(WrongLocoDescriptor, Error, "Loco parameter is not a LocoDescriptor type")

# same as: class WrongJsonData(Error):
new_exception(WrongJsonData, Error, "Data provided is not a valid JSON file")
