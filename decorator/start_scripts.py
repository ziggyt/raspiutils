import atexit
import subprocess
import sys
from time import sleep
from signal import signal, SIGINT

import gpiozero

print("Started main controller")
main_controller_process = subprocess.Popen(["python3", "main_controller.py"])
sleep(0.2)
print("Started server")
server_process = subprocess.Popen(["python3", "server.py"])

used_pins = [17, 27, 22, 10]


def turn_off_all_relays():
    for pin in used_pins:
        a = gpiozero.OutputDevice(pin)
        a.on()
        print(f"Turned off relay at pin {pin}")

@atexit.register
def shutdown():
    print("Killed scripts")
    main_controller_process.terminate()
    server_process.terminate()
    turn_off_all_relays()
    sys.exit()


signal(SIGINT, shutdown)

while True:
    sleep(1)
