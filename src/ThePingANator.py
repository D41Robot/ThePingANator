#/*******************************************************************
#* File Name         : ThePingANator.Py
#* Description       : Little GUI that will ping deivces and report indicator or response
#* Version           : 0.0.2
#*                    
#* Revision History  :
#* Date		Version    Author 			Comments
#* ------------------------------------------------------------------
# 11/03/2024	0.0.1   D41Robot        Initial Release
# 11/03/2024    0.0.2   D41Robot        Group Labels Functioning
#
#/******************************************************************/
from concurrent.futures import thread
import tkinter as tk
import time
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
#Positions relates to Group value in user_inputs
group_names = ['Internal', 'External']

#GUI behavior settings
#Glogal font and size for labels
global_font = "tkDefaeultFont"
global_font_size = 10
#How often the GUI refreshes in seconds
refresh_rate = 0.5
#Controls paddinding for tkinter
global_padx = 5
global_pady = 5
#Turn on or off Group Label, 1 = ON, 0 = OFF
group_label_option = 1

#DONE WITH USER INPUTS

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
app_stats = [None,None,None]
space_count = 1

#Main state machine value
control_state = 0

#Not 100% sure what you do but it works
update_queue = queue.Queue()

#Conbtrol functions
def start_indicators():
    global control_state
    control_state = 1
    app_stats[0].config(bg='green')
    print("START PING")

def stop_indicators():
    global control_state
    control_state = 0
    app_stats[0].config(bg='yellow')
    print("STOP PING")

def exit_app():
    global control_state
    control_state = 2
    app_stats[0].config(bg='red')
    print("QUIT ENTERED")

#Clock function
def update_clock():
    # get current time as text
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    # udpate text in clock Label
    app_stats[2].config(text=current_time)
   
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
#Working, could be better
def group_row_spacing(index):
    global space_count
    prev_space_count = space_count
    count = 1
    for x in range(len(user_inputs)):
        if int(user_inputs[x]["Group"]) == int(index):
            count = count + 1     
    space_count = count + space_count
    return prev_space_count

#Main
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        #Create Canvas and basic elements
        self.create_widgets()

        #What does everything
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
                print("QUITTING FOR REAL")
                quit()

            else:
                print("YEET, TAKE THE WHEEL")
                quit()


            while not update_queue.empty() and control_state == 1:
                index, status_text, color = update_queue.get()
                my_indicator[index].config(text=status_text, bg=color)

            update_clock()   
            self.update()  # Update the complete GUI.
            print("Panel Loop Complete")
            time.sleep(refresh_rate)

    def create_widgets(self):
        #Create Canvas
        self.geometry()
        self.title(title_banner)
        self.resizable(0, 0)
        
        #Create column heading
        for x in range(len(column_headers)):
            column_headers_labels[x] = tk.Label(master=self, text=column_headers[x], font=(global_font, global_font_size), bg='white', fg='black')
            column_headers_labels[x].grid(column=x, row=0, sticky=tk.NS, padx=global_padx, pady=global_pady)
            
        #Create each label for user_inputs
        for x in range(len(user_inputs)): #Create labels for the names of what is getting pingged
            label_names[x] = tk.Label(self, text=user_inputs[x]["Name"], font=(global_font, global_font_size), bg='white',fg='black')
            label_names[x].grid(column=0, row=x+(user_inputs[x]["Group"]*1)+2, sticky=tk.W, padx=global_padx, pady=global_pady)
        for x in range(len(user_inputs)): #Create lebels with address of what is getting pingged
            label_addresses[x] = tk.Label(self, text=user_inputs[x]["Address"], font=(global_font, global_font_size), bg='white',fg='black')
            label_addresses[x].grid(column=1, row=x+(user_inputs[x]["Group"]*1)+2, sticky=tk.W, padx=global_padx, pady=global_pady)
        for x in range(len(my_indicator)): #Create items that will be updated based on ping status, default state
            my_indicator[x] = tk.Label(master=self, text="IDLE", font=(global_font, global_font_size), bg='white', fg='Black')
            my_indicator[x].grid(column=2, row=x+(user_inputs[x]["Group"]*1)+2, sticky=tk.NS, padx=global_padx, pady=global_pady)

        #App Status Stuff
        app_stats[0] = tk.Label(master=self, text="APP STATUS", font=(global_font, global_font_size), bg='white',fg='black')
        app_stats[0].grid(column=0,row=len(user_inputs)+len(group_names)+1, sticky=tk.W, padx=global_padx, pady=global_pady)
        app_stats[1] = tk.Label(master=self, text="Last update time:", font=(global_font, global_font_size), bg='white',fg='black')
        app_stats[1].grid(column=1,row=len(user_inputs)+len(group_names)+1, sticky=tk.W, padx=global_padx, pady=global_pady)
        app_stats[2] = tk.Label(master=self, text=datetime.datetime.now().strftime("%H:%M:%S.%f"), font=(global_font, global_font_size), bg='cyan',fg='black')
        app_stats[2].grid(column=2,row=len(user_inputs)+len(group_names)+1, sticky=tk.NS, padx=global_padx, pady=global_pady)
        
        #Control buttons
        start_button = tk.Button(self, text="START PING", font=(global_font, global_font_size), command=start_indicators) 
        start_button.grid(column=0, row=len(user_inputs)+len(group_names)+2, sticky=tk.NS, padx=global_padx, pady=global_pady)
        stop_button = tk.Button(self, text="STOP PING", font=(global_font, global_font_size), command=stop_indicators)   
        stop_button.grid(column=1, row=len(user_inputs)+len(group_names)+2, sticky=tk.NS, padx=global_padx, pady=global_pady)
        exit_button = tk.Button(self, text="EXIT", font=(global_font, global_font_size), command=exit_app) 
        exit_button.grid(column=2, row=len(user_inputs)+len(group_names)+2, sticky=tk.NS, padx=global_padx, pady=global_pady)

        #Group Labels
        if (group_label_option == 1):
            for x in range(len(group_names)):
                group_label[x] = tk.Label(master=self, text=group_names[x], bg='pink', fg='black')
                group_label[x].grid(column=0, row=int(group_row_spacing(x)), columnspan=len(column_headers), sticky=tk.NS, padx=global_padx, pady=global_pady)

if __name__ == "__main__":
    app = App()
    app.mainloop()