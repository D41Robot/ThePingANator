# ThePingANator
Tool designed to ping multiple targets on a single process instead of multiple terminals opened at the same time.

# Add Ping Locaions
The following block can ben added to user_inputer for additional ping locations.

    {
        "Name": "Router",
        "Address": "192.168.1.1",
        "Group": 0,
    },

Name: What the item is called  
Address: IP Address on the newtork   
Group: Way to break up the GUI into sections  

# Application Use
There is 3 control buttons offered in the application

START PING:
    Start the ping process  
    Changes APP_STAUTS to green  

STOP PING:
    Stops the ping process but keeps the application running so it can be started again, IDLE state  
    Changes APP_STAUTS to yellow  
    Note: Returns all status to IDLE  

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
