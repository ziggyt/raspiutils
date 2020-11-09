from datetime import datetime, timedelta

import gpiozero


class RelayModule:

    def __init__(self, pin: int, name: str):
        self.pin = pin
        self.name = name
        self.output_pin = gpiozero.OutputDevice(pin=self.pin)

    def turn_on(self):
        print(f"Turned on {self.name}")
        self.output_pin.off()

    def turn_off(self):
        if self.is_on():
            print(f"Turned off {self.name}")
            self.output_pin.on()

    def is_on(self):
        return not self.output_pin.value

    def __str__(self) -> str:
        return f"{self.name} state: {self.is_on()}"


class TimerRelayModule(RelayModule):

    def __init__(self, pin: int, name: str, start_time: int, end_time: int):
        super().__init__(pin, name)
        self.start_time = datetime(year=2000, day=1, month=1, hour=start_time, minute=0)
        self.end_time = datetime(year=2000, day=1, month=1, hour=end_time, minute=0)

    def should_turn_on(self):
        now = datetime.now()
        return self.start_time.hour <= now.hour < self.end_time.hour and not self.is_on()

    def should_turn_off(self):
        now = datetime.now()
        return not (self.start_time.hour <= now.hour < self.end_time.hour) and self.is_on()


class IntervalRelayModule(RelayModule):

    def __init__(self, pin: int, name: str, duration: int, time_between: int):
        super().__init__(pin, name)
        self.duration = duration
        self.time_between = time_between
        self.last_turned_on = datetime.now() - timedelta(
            hours=12)  # todo why did you do this? i guess it was to make sure that it always turns on as default

    def turn_on(self):
        super().turn_on()
        now = datetime.now()
        self.last_turned_on = now

    def should_turn_on(self):
        now = datetime.now()
        return (now - self.last_turned_on).seconds >= self.duration and now >= (
                    self.last_turned_on + timedelta(seconds=self.time_between)) and not self.is_on()

    def should_turn_off(self):
        if self.last_turned_on is None:
            return False

        now = datetime.now()
        if now >= self.last_turned_on + timedelta(seconds=self.duration) and self.is_on():
            return True

    def uptime(self):
        now = datetime.now()
        return (now - self.last_turned_on).seconds
