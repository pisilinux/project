Service Manager
---------------

**Service Manager** is the Pardus Project you can use to manage services's status and their start options. A service's status may be running or stopped and its start option can be set as 'Run on startup' or not. If a service is running, it can serve something related to its job otherwise it is stopped and serves nothing.


Listing And Searching Services
------------------------------

When you open the Service Manager you see a list in the center and bottom of the window. This list is used for to display services on the system. Initially, Service Manager lists all Servers, no matter if they are stopped or running, on the system. If you want to list only running services on your system select 'Running Services' from the combo box at the right side of the top of the window. You also select and list System Services, Startup Services, All Services from this check box. 
There is a text box at the left side of the top of the list. You can search a specific service by typing the name of it there.


Starting a Service
------------------

You can understand if a service is running or stopped by looking the icon for that service near the name of it on the list. If the icon is a red flag it is stopped otherwise its icon is a green flag and this means the service is runnig. 
In order to start a service move your mouse on it on the list and when the mouse comes over it a group of widgets appears on the right side of the item. You can start the service by clicking the 'Start' (first) button. Pardus asks for root password to start service, enter it. Now the service is started, you can see how its flag icon turns red to green.
Once a service is started it starts to serve its job.

Stopping a Service
------------------

You can understand if a service is running or stopped by looking the icon for that service near the name of it on the list. If the icon is a red flag it is stopped otherwise its icon is a green flag and this means the service is runnig. 
In order to stop a service move your mouse on it on the list and when the mouse comes over it a group of widgets appears on the right side of the item. You can stop the service by clicking the 'Stop' (third) button. Pardus asks for root password to stop service, enter it. Now the service is stopped, you can see how its flag icon turns green to red.


Restarting a Service
--------------------

In order to restart a service move your mouse on it on the list and when the mouse comes over it a group of widgets appears on the right side of the item. You can restart the service by clicking the 'Restart' (second) button. Pardus asks for root password to restart service, enter it. Now the service is restarted.


Starting Services Automatically at Startup
------------------------------------------

Some services starts automatically when the system starts. We call this as 'auto start' property of a service.
In order to set a service's auto start property move your mouse on it on the list and when the mouse comes over it a group of widgets appears on the right side of the item. You can add auto start property to a service by checking the 'Run on startup'check box. Pardus asks for root password to add this property to the service, enter it. Once a service has gained the auto start property it starts automatically after first reboot. You can remove auto start propert by unchecking the check box.
