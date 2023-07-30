Touchless PC volume controller arduino project.

<h1>V1</h1> 
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


<h1>V2</h1>
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


Components used:
- Arduino nano
- US-100 ultrasonic distance sensor
- ZS-040 bluetooth module