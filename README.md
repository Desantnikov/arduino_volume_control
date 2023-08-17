<h1>Touchless PC volume controller arduino project.</h1>
<h2>
No need to touch stuff anymore. Adjust volume just by swinging your hand. 
</h2>

Basically you just place your hand inside this box and swing it up and down. And volume 
is changes according to your hand's Y position.  
Volume control and media play/pause will work only on windows 

<pre>
_____-
|
|
|
|
|
|
|
|
—   --
| ^  |
| 1* |
——----
</pre>

`1*` - distance sensor with measurement direction marked by ^ 

Main idea is to place a distance sensor inside the box. Distance sensor should 
be fixed on the bottom of the box. Distance measurements should be directed from box bottom to box top. 
Measurements happen several times per second. 
If currently measured distance equals to overall box height - it means that there
are no obstacles between the bottom and the top. But if measured distance is less than overall box 
height - it means that something is present in the box. And using measured distance we know it's
exact position on the Y coord. Then measurements values are sent to PC to adjust volume accordingly  



<h1>Version 1</h1> 
<h2>
Uses firmata protocol to fully control arduino from PC. 
No arduino code, all measurement values go directly to python script 
</h2> 


Sketch from examples of FirmataExpress arduino lib is uploaded on arduino. It fully implements firmata protocol
and gives ability to do all the shit you would want to do inside the arduino sketch. Allows not only setting 
pins HIGH or LOW, but also provides handy wrappers for many types of detectors. Everything is good 
except wired connection necessity.
Don't forget to set correct pins in the `/v1/constants.py`

Components used:
- Arduino nano
- US-015 ultrasonic distance sensor
<hr>


<h1>Version 2</h1>
<h2>
Uses better distance sensor and bluetooth module to send measurement results.
</h2>

Uses better distance sensor US-100, which supports UART mode and accepts commands instead
of setting and reading pins voltage directly. Also it has a built-in thermometer, which is not used in this
project. After first tests I could say that it works better than US-015.
Uses ZS-040 bluetooth module to send measurement results. Please note that before connecting it has to be
switched to the AT mode. To check if it's switched - open serial terminal and type "AT". And don't forget to set 
both CR and LF endlines. Official doc says that default connection password is "000000". In my case it was "1234".
All baudrates should be 9600, but in case of any issues you might try 38400.

SW_520D tilt-switch sensor is used to track when user hit the controller. And if hit two 
times - plays/pauses what is currently playing
Curcuits schema can be found in /v2/circuits, `*.fxx` is a Fritzing applications format. Have much more 
components (like US-100 or ZA-40) than tinkercad, circuitIO and other webapp shit.   
![AdruinoVolumeController_bb.jpg](v2%2Fcircuits%2FAdruinoVolumeController_bb.jpg)

Lots of workarounds were used in python code and in arduino sketch. But these workarounds really improved 
the measurement process and made controlling PC with this stuff more or less smooth.

Python W/A's
1. When processing data from distance sensor - ignore fluctuations of less than 5% of volume
2. When registering doubleclick with vibration sensor 
   3. ignore vibros if they happened right after previous vibro - 
      usually that happens when sensor is not placed properly or instead of clicks user makes long pushes
   4. ignore doubleclick if second vibro happened too late after first vibro  
   5. ignore doubleclick if it happened too early after previous - same as 3th point

Similiar workarounds were made on the Arduino side.
Main question here is how this all will work when soldered. Maybe more workarounds will be needed. Or to rework 
using vibro sensor to read pin in a main loop instead of using interruptions


Components used:
- Arduino nano
- US-100 ultrasonic distance sensor
- ZS-040 bluetooth module
- SW18010P vibration sensor (initially took SW-520D, but I don't need a tilt sensor)
- 9v battery (to be replaced with 5v power supply, distance sensor goes crazy when 9v applied)





<h1>Making and *.exe file</h1>
* make sure you have installed microsoft visual c++ 2015
* make sure you have installed gevent package
* execute `auto-py-to-exe`