### ### ### ### ###
# functions.py
# contains extra functions to support TCP
# comunication as well as extra tasks
# moving extra functions here improves
# readability of main.py
### ### ### ### ###

import mem
import WiDCCProtocol

# read and send helper functions for transmitting 
# data over TCP
def f_tcp_send_msg(msg):
    # transmit a full message over TCP
    # it checks if the message is fully 
    # transmitted, if not reiterates
    msg_len = len(msg)
    sent_len = 0
    while sent_len < msg_len:
        buf_len = mem.my_socket.send(msg[sent_len:])
        sent_len += buf_len

def f_tcp_feedback_msg():
    # waits for the server reply - blocking!!!
    # check if the setblocking(False) works
    
    data = mem.my_socket.recv(128)
    sent_len = len(data)
    while sent_len:
        buf = mem.my_socket.recv(128)
        data += buf
        sent_len = len(buf)
         
    return data




# function to be threaded that handle communication
# over tcp
def f_tcp_communication():
    print("tcp_communication start")
    
    # do I need lock on the socket to prevent
    # simultaneous connections attempt?
    mem.my_socket_lock.acquire()
    print("tcp_communication lock acquired")
    mem.my_socket.connect(mem.my_config.server)
    if mem.msg_queue_out.isEmpty():
        # send messageAlive
        msg = WiDCCProtocol.create_message(mem.my_loco, WiDCCProtocol.MsgTypes.ALIVE )          
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
        mem.msg_queue_out_lock.acquire()
        msg = WiDCCProtocol.create_message(mem.my_loco, mem.msg_queue_out.get() )
        mem.msg_queue_out_lock.release()    
        f_tcp_send_msg(msg)
    mem.my_socket_lock.release()

    # every 3 transmission automtically send a
    # Status message    
    if mem.my_com_timer_counter >= 3:
        mem.my_com_timer_counter = 0
        mem.msg_queue_out_lock.acquire()
        mem.msg_queue_out.insert( WiDCCProtocol.MsgTypes.STATUS )
        mem.msg_queue_out_lock.release()
    
    mem.my_com_timer_counter += 1
            
    # wait for the reply
    msg = f_tcp_feedback_msg()
    message = WiDCCProtocol.read_message(msg)
    if not message.msg_type == WiDCCProtocol.MsgTypes.ACK:
        mem.msg_queue_in_lock.acquire()
        mem.msg_queue_in.put(message)
        mem.msg_queue_in_lock.release()
        
    print("tcp_communication end")        

# execute the instruction provided with a message 
def f_exec_msg(msg):
    elif msg_type == WiDCCProtocol.MsgTypes.REGISTERED:
        # this message type is discrded in this
        # state. it isonly considered at startup
        pass
    elif msg_type == WiDCCProtocol.MsgTypes.CONFIG:
        # set loco id, max speed, and train mass
        pass
    elif msg_type == WiDCCProtocol.MsgTypes.STATUS:
        # if this command is received somethig is 
        # wrong the "Status" is only sent.
        pass
    elif msg_type == WiDCCProtocol.MsgTypes.COMMAND:
        # here is something to do
        pass
    elif msg_type == WiDCCProtocol.MsgTypes.EMERGENCY:
        # power off the motors
        pass
    elif msg_type == IDENTIFY:
        # activate the identify blinking pattern
        pass        
    else:
        pass


# read and implement incoming messages
def f_run_read_msg():
    # once this function is reached better to clear 
    # the message_in list to prevent overflow and to 
    # execute the latest command in case 2 different 
    # commands have been submitted in a row
    print("run_read_message: %s unread", mem.msg_queue_in.elements() )
    while not mem.msg_queue_in.isEmpty():
        msg = mem.msg_queue_in.get()
        print("Received message %s", msg.msg_type)
        f_exec_msg(msg)
  
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
  
