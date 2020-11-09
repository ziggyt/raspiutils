import time
import board
import adafruit_dht #needs to be installed on raspi


class DhtDevice:

    def __init__(self, pin: board.pin) -> None:
        self.pin = pin
        self.dht_device = adafruit_dht.DHT22(self.pin)
        self.last_msg = None

    def print_error_info(self, msg):
        if msg != self.last_msg:
            print(msg)
            self.last_msg = msg

    def get_temperature(self):

        temp = 0

        while temp is 0:
            try:
                # Print the values to the serial port
                temp = self.dht_device.temperature

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                self.print_error_info(error.args[0])
                continue

            except:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print("Something went wrong with dht sensor")
                continue

            time.sleep(2)

        return temp

    def get_humidity(self):

        hum = 0

        while hum is 0:
            try:
                # Print the values to the serial port
                hum = self.dht_device.humidity

            except RuntimeError as error:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                self.print_error_info(error.args[0])

                continue

            except:
                # Errors happen fairly often, DHT's are hard to read, just keep going
                print("Something went wrong with dht sensor")
                continue

            time.sleep(2)

        return hum
