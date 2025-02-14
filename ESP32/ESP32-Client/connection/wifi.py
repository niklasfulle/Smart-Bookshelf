"""
    -
"""
# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R1705
import time

import network  # noqa: F401 # type: ignore
from machine import Pin  # noqa: F401 # type: ignore
from network import WLAN  # noqa: F401 # type: ignore

# Function to connect to a specific wifi network
def wifi(essid, password, timeout):
    """ der esp32 verbindet sich mit dem WLAN

    Args:
        essid: die SSID vom WLAN
        password: das Passwort mit vom WLAN
        timeout: Zeit die gewarted wird auf die Verbindung

    Returns:
        ob die Verbindung aufgebaut wurde
    """
    wlan = WLAN(network.STA_IF)  # create station interface
    wlan.active(True)

    if not wlan.isconnected():
        led = Pin(2, Pin.OUT)
        print("Connecting to WiFi network...")
        wlan.connect(essid, password)
        # Wait until connected
        t = time.ticks_ms()
        while not wlan.isconnected():
            if time.ticks_diff(time.ticks_ms(), t) > timeout:
                wlan.disconnect()
                print("Timeout. Could not connect.")
                while not wlan.isconnected():
                    led.value(1)
                    time.sleep(0.2)
                    led.value(0)
                    time.sleep(0.2)
                    led.value(1)
                    time.sleep(1)
                    led.value(0)
                    time.sleep(0.2)
                return False

        print("Successfully connected to " + essid)
        #print(wlan.ifconfig())
        return True
    else:
        print("Already connected")
        return True
