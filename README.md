# ThePingANator
Tool designed to ping multiple targets on a single process instead of multiple terminals opened at the same time.

# Add Ping Locaion(s)
The following block can ben added to user_inputer for additional ping locations.

    {
        "Name": "Router",
        "Address": "192.168.1.1",
        "Group": 0,
    },

Name: What the item is called  
Address: IP Address that will be pingged 
Group: Way to break up the GUI into sections. Value comes from the intended group position if group_names

# Add Group(s)
Groups can be used to break up the GUI with different section. Additional elements can be added for groups. Item index number is associated with with ping location will fall under that tag.

    group_names = ['Internal', 'External']

# GUI Behvaior Settings
The following settings are available for the user to change.

    #GUI BEHAVIOR SETTING
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

# Application Use
There is 3 control buttons offered in the application

START PING:
    Start the ping process  
    Changes APP_STAUTS to green  

STOP PING:
    Stops the ping process but keeps the application running so it can be started again, IDLE state  
    Changes APP_STAUTS to yellow  
    Note: Returns all PING STATUS to IDLE  

EXIT: 
    Stops the application
    Changes APP_STATUS to red  
    Note: may take a few seconds to close as residual pings finish  

# PING STATUS Explincation
Response of 

IDLE: The application just started or ping process is not running

GOOD: Ping to the device was suscessful

BAD: Ping to the device ws not suscessful 

ERROR: Something really bad happened to the ping subprocesses

# APP STATUS Explination
There is 4 main states of the GUI indicated by the color of the APP STATUS box

White:
    Application just started  
    ![white](/Photos/WHITE.png)

Green:
    Appplication is pining devices  
    ![green](/Photos/GREEN.png)

Yellow
    Application is in the IDLE state  
    ![yellow](/Photos/YELLOW.png)

Red
    Appliation is in the process of shutting down  
    ![red](/Photos/RED.png)

# To Do List  
Improve GUI Response