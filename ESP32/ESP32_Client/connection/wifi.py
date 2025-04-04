"""
-
"""

# pylint: disable-msg=W0603,W0718,E1101,C0209,E0401,E0611,W0105,R0903,R0913,W0622,R1705
import time

import network  # noqa: F401 # type: ignore
from machine import Pin  # noqa: F401 # type: ignore
from network import WLAN  # noqa: F401 # type: ignore


def wifi(essid, password, timeout):
    """
    Connects to a WiFi network using the provided ESSID and password.
    This function attempts to establish a connection to a WiFi network
    using the given ESSID (network name) and password. If the connection
    is not successful within the specified timeout period, it disconnects
    and enters a loop to indicate the failure using an LED.
    Args:
        essid (str): The name of the WiFi network (SSID) to connect to.
        password (str): The password for the WiFi network.
        timeout (int): The maximum time (in milliseconds) to wait for a connection.
    Returns:
        bool: True if the connection is successful, False otherwise.
    Behavior:
        - If the device is already connected to a WiFi network, it will
          print a message and return True immediately.
        - If the connection attempt times out, the function will blink
          an LED in a specific pattern to indicate failure and return False.
        - If the connection is successful, it will print a success message
          and return True.
    """

    wlan = WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        led = Pin(2, Pin.OUT)
        print("Connecting to WiFi network...")
        wlan.connect(essid, password)

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

        return True
    else:
        print("Already connected")
        return True
