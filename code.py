#   v0.91
#   7/8/2023  Dave Thompson

#
import time
import board
import busio
import terminalio
import digitalio
from adafruit_binascii import hexlify
from adafruit_matrixportal.matrixportal import MatrixPortal

# --- Display setup ---
matrixportal = MatrixPortal(
    width=128, height=64, status_neopixel=board.NEOPIXEL, debug=True
)

uart = busio.UART(board.TX, board.RX, baudrate=9600)
uart.reset_input_buffer()  # flush input buffer


def ReadSample():
    """
    Q&A mode requires a command to obtain a reading sample
    Returns: int PM1, int PM25, int PM10
    """
    uart.reset_input_buffer()
    uart.write(b"\xFF\x01\x86\x00\x00\x00\x00\x00\x79")
    reading = ((hexlify(uart.read(2))), 16)
    PM1 = int((hexlify(uart.read(2))), 16)
    PM25 = int((hexlify(uart.read(2))), 16)
    PM10 = int((hexlify(uart.read(2))), 16)
    CO2 = int((hexlify(uart.read(2))), 16)
    VOC = int((hexlify(uart.read(1))), 16)
    TEMP = int((hexlify(uart.read(2))), 16)
    HUM = int((hexlify(uart.read(2))), 16)
    CH2O = int((hexlify(uart.read(2))), 16)
    CO = int((hexlify(uart.read(2))), 16)
    O3 = int((hexlify(uart.read(2))), 16)
    NO2 = int((hexlify(uart.read(2))), 16)
    return (PM1, PM25, PM10, CO2, VOC, TEMP, HUM, CH2O, CO, O3, NO2)


PM1, PM25, PM10, CO2, VOC, TEMP, HUM, CH2O, CO, O3, NO2 = ReadSample()

# PM1 - label 0
matrixportal.add_text(text_font=terminalio.FONT, text_position=(1, 5), text_scale=0.01)

# PM25 label 1
matrixportal.add_text(text_font=terminalio.FONT, text_position=(1, 15), text_scale=0.01)
# PM10 label 2
matrixportal.add_text(text_font=terminalio.FONT, text_position=(1, 25), text_scale=0.01)

#  CO2 label 3
matrixportal.add_text(text_font=terminalio.FONT, text_position=(1, 35), text_scale=0.01)
#  Temp label 4
matrixportal.add_text(text_font=terminalio.FONT, text_position=(1, 45), text_scale=0.01)
#  Humidity label 5
matrixportal.add_text(text_font=terminalio.FONT, text_position=(1, 55), text_scale=0.01)

#   CH2O label 6
matrixportal.add_text(text_font=terminalio.FONT, text_position=(64, 5), text_scale=0.01)

#   CO label 7
matrixportal.add_text(
    text_font=terminalio.FONT, text_position=(64, 15), text_scale=0.01
)

#   O3 label 8
matrixportal.add_text(
    text_font=terminalio.FONT, text_position=(64, 25), text_scale=0.01
)

#   NO2 label 9
matrixportal.add_text(
    text_font=terminalio.FONT, text_position=(64, 35), text_scale=0.01
)

#   Time label 10
matrixportal.add_text(
    text_font=terminalio.FONT, text_position=(64, 45), text_scale=0.01
)

# Color Palette
Default = "#1665da"  # Blue
OK = "#0bef46"  # Green
ELEV = "#bcef0b"  # YEL
HIGH = "#ef8e0b"  # ORG
WARN = "#f02207"  # RED
BAD = "#6507f0"  # PURP
VBAD = " "  # WHT

while True:
    try:

        PM1, PM25, PM10, CO2, VOC, TEMP, HUM, CH2O, CO, O3, NO2 = ReadSample()

        if PM25 < 51:
            pm25_color = OK
        elif PM25 < 101:
            pm25_color = ELEV
        elif PM25 < 151:
            pm25_color = HIGH
        elif PM25 < 200:
            pm25_color = WARN
        elif PM25 < 300:
            pm25_color = BAD
        elif PM25 > 301:
            pm25_color = VBAD

        if PM10 < 149:
            pm10_color = OK
        elif PM10 > 101:
            pm10_color = BAD

        if CO2 < 599:
            CO2_color = OK
        elif CO2 < 799:
            CO2_color = ELEV
        elif CO2 < 1000:
            CO2_color = HIGH
        elif CO2 < 1200:
            CO2_color = BAD

        # PM1
        matrixportal.set_text("PM1   " "%d" % PM1, 0)
        matrixportal.set_text_color(pm25_color, 0)

        # PM25
        matrixportal.set_text("PM2.5 " "%d" % PM25, 1)
        matrixportal.set_text_color(pm25_color, 1)

        # PM10
        matrixportal.set_text("PM10  " "%d" % PM10, 2)
        matrixportal.set_text_color(pm10_color, 2)

        # CO2
        matrixportal.set_text("CO2   " "%d" % CO2, 3)
        matrixportal.set_text_color(CO2_color, 3)

        # Temp
        matrixportal.set_text("T  " "%.2f" % ((((TEMP - 500) * 0.1) * 1.8) + 32), 4)
        matrixportal.set_text_color(OK, 4)

        # Humidity
        matrixportal.set_text("H  " "%d" % HUM, 5)
        matrixportal.set_text_color(OK, 5)

        # Formaldehyde
        matrixportal.set_text("CH20 " "%.3f" % (CH2O * 0.001), 6)
        matrixportal.set_text_color("#1665da", 6)

        # Carbon Monoxide
        matrixportal.set_text("CO   " "%.1f" % (CO * 0.1), 7)
        matrixportal.set_text_color("#1665da", 7)

        # Ozone
        matrixportal.set_text("O3   " "%.2f" % (O3 * 0.01), 8)
        matrixportal.set_text_color("#1665da", 8)

        # Nitrous Oxide
        matrixportal.set_text("NO2  " "%.3f" % (NO2 * 0.001), 9)
        matrixportal.set_text_color("#1665da", 9)

        print(PM1)
        print(PM25)
        print(PM10)
        print(CO2)
        print(VOC)
        print((TEMP - 500) * 0.1)
        print(HUM)
        print(CH2O * 0.001)
        print(CO * 0.1)
        print(O3 * 0.01)
        print(NO2 * 0.001)
        print("----------")
    except (ValueError, RuntimeError) as e:
        print("Some error occured, retrying! -", e)

    # time.sleep(3 * 60)  # wait 3 minutes
    time.sleep(10)
