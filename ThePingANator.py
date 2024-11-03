import tkinter as tk
import time
from xmlrpc.client import boolean
from ping3 import ping, verbose_ping
import datetime
import threading
import subprocess
import platform
import queue

#What are you looking to ping?
#Name: What the item is called,
#Address: IP Address on the newtork, 
#Group: Way to break up the GUI into sections
user_inputs = [
    {
        "Name": "Router",
        "Address": "192.168.1.1",
        "Group": 0,
    },
    {
        "Name": "Google",
        "Address": "google.com",
        "Group": 1,
    }    
]

#Group Labels
#Positions relates to Group in user_inputer
group_names = ['Internal', 'External']

#DONE WITH COMMON USER INPUTS

#IDK If you want to change what it says on the top
column_headers = ['NAME', 'ADDRESS', 'PING STATUS']
title_banner = ['ThePingANator']

#Variables
ping_response = [None] * len(user_inputs)
my_indicator = [None] * len(user_inputs)
label_addresses = [None] * len(user_inputs)
label_names = [None] * len(user_inputs)
column_headers_labels = [None] * len(column_headers)
group_label = [None] * len(group_names)
clock_label = [None,None]
#Main state machine value
control_state = 0
#Controls paddinding for tkinter
global_padx = 5
global_pady = 5
#Not 100% sure but it works
update_queue = queue.Queue()

#Conbtrol functions
def start_indicators():
    global control_state
    control_state = 1
    clock_label[0].config(bg='green')
    print("START PING")

def stop_indicators():
    global control_state
    control_state = 0
    clock_label[0].config(bg='yellow')
    print("STOP PING")

def exit_app():
    global control_state
    control_state = 2
    clock_label[0].config(bg='red')
    print("QUIT")
    quit()

#Clock function
def update_clock():
    # get current time as text
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    # udpate text in Label
    clock_label[1].config(text=current_time)
    #lab['text'] = current_time

#ping fuction
def ping_address_subprocess(address, index):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', address]
    
    try:
        response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if response.returncode == 0:
            print(f"Response from {address}: Successful")
            update_queue.put((index, "GOOD", 'green'))
        else:
            print(f"No response from {address}")
            update_queue.put((index, "BAD", 'red'))
    except Exception as e:
        print(f"Error pinging {address}: {e}")
        update_queue.put((index, "ERROR", 'orange'))

#Group Spacing Function
def group_row_spacing(name):
    return name

#Main
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Create Canvas and basic elements
        self.create_widgets()

        #What does really everything
        while(1):
            if(control_state == 1):
                for x in range(len(user_inputs)):
                    threading.Thread(target=ping_address_subprocess, args=(user_inputs[x]["Address"], x)).start()
                print("Pinging addresses...")
                          
            elif(control_state == 0): #Set circles back to default
                for x in range(len(user_inputs)):
                    my_indicator[x].config(text="IDLE", bg='white', fg='Black')
                print("GUI Default")

            elif(control_state == 2):
                print("QUIT")
                quit()

            else:
                print("YEET, TAKE THE WHEEL")
                quit()

            while not update_queue.empty():
                index, status_text, color = update_queue.get()
                my_indicator[index].config(text=status_text, bg=color)

            update_clock()   
            self.update()  # Update the complete GUI.
            print("Panel Loop Complete")
            time.sleep(0.5)

    def create_widgets(self):
        #Create Canvas
        self.geometry()
        self.title(title_banner)
        self.resizable(1, 1)
        
        #Create column heading
        for x in range(len(column_headers)):
            column_headers_labels[x] = tk.Label(master=self, text=column_headers[x], bg='white', fg='black')
            column_headers_labels[x].grid(column=x, row=0, sticky=tk.NS, padx=global_padx, pady=global_pady)

        #Create labels for the names of what is getting pingged
        for x in range(len(user_inputs)):
            label_names[x] = tk.Label(self, text=user_inputs[x]["Name"], bg='white',fg='black')
            label_names[x].grid(column=0, row=x+user_inputs[x]["Group"]+2, sticky=tk.W, padx=global_padx, pady=global_pady)
            
        #Create lebels with address of what is getting pingged
        for x in range(len(my_indicator)):
            label_addresses[x] = tk.Label(self, text=user_inputs[x]["Address"], bg='white',fg='black')
            label_addresses[x].grid(column=1, row=x+user_inputs[x]["Group"]+2, sticky=tk.W, padx=global_padx, pady=global_pady)

        #Create items that will be updated based on ping status, default state
        for x in range(len(my_indicator)):
            my_indicator[x] = tk.Label(master=self, text="IDLE", bg='white', fg='Black')
            my_indicator[x].grid(column=2, row=x+user_inputs[x]["Group"]+2, sticky=tk.NS, padx=global_padx, pady=global_pady)

        #Clock Stuff
        clock_label[0] = tk.Label(master=self, text="Last update time: ", bg='white',fg='black')
        clock_label[0].grid(column=0,row=len(user_inputs)+len(group_names)+2, sticky=tk.W, padx=5, pady=5)
        clock_label[1] = tk.Label(master=self, text=datetime.datetime.now().strftime("Time: %H:%M:%S%f"), bg='cyan',fg='black')
        clock_label[1].grid(column=1,row=len(user_inputs)+len(group_names)+2, sticky=tk.W, padx=global_padx, pady=global_pady)
        
        #Control buttons
        start_button = tk.Button(self, text="START PING", command=start_indicators) 
        start_button.grid(column=0, row=len(my_indicator)+len(group_names)+3, sticky=tk.NS, padx=global_padx, pady=global_pady)
        stop_button = tk.Button(self, text="STOP PING", command=stop_indicators)   
        stop_button.grid(column=1, row=len(my_indicator)+len(group_names)+3, sticky=tk.NS, padx=global_padx, pady=global_pady)
        exit_button = tk.Button(self, text="EXIT", command=exit_app) 
        exit_button.grid(column=2, row=len(my_indicator)+len(group_names)+3, sticky=tk.NS, padx=global_padx, pady=global_pady)

        #Somehow we make different sections happen here
        #Disabled Group labels until we can find a way to make it work
        #for x in range(len(group_names)):
        #    group_label[x] = tk.Label(master=self, text=group_names[x], bg='pink', fg='black')
        #    group_label[x].grid(column=0, row=group_row_spacing(x), columnspan=len(column_headers), sticky=tk.NS, padx=global_padx, pady=global_pady)

if __name__ == "__main__":
    app = App()
    app.mainloop()