### ### ### ### ###
# functions.py
# contains extra functions to support TCP
# comunication as well as extra tasks
# moving extra functions here improves
# readability of main.py
### ### ### ### ###

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
  

