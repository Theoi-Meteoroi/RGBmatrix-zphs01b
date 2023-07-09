# RGBmatrix-zphs01b
Circuit Python implementation of 64x128 RGBmatrix display for Winsen zphs01b multisensor module

This project uses the Adafruit MatrixPortal M4 serial port to display sensor readings from a Winsen ZPHS01B, a multi-in-one air quality module, integrating laser dust sensor, infrared carbon dioxide sensor, electrochemical formaldehyde sensor, electrochemical ozone sensor, electrochemical carbon monoxide sensor, VOC sensor, NO2 sensor and temperature and humidity sensor. It has a UART ( 3.3v TTL level) communication interface.

The MatrixPortal M4 is pretty handy - providing +5v power to both 64x64 panels as well as the sensor module board. A USB-C port provides power to the entire project. This allows the display to stand-alone, readable from a distance.  The code is written using CircuitPython 8.1 and uses libraries from the 8.x bundle. A secrets file is required by the MatrixPortal libraries to connect to Wifi, even though the code doesn't use it, yet.  

To store the data produced - the MatrixPortal allows connecting to local WiFi and then to a MQTT broker, like AdafruitIO.  The section at the bottom of the loop can be converted to mqtt topics.
