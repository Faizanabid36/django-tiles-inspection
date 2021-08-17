from gpiozero import LED


class Signalling:

    def __init__(self, threshold = 0.5):
        self.threshold = threshold
        self.red = LED(26)
        self.yellow = LED(19)
        self.green = LED(13)

    def signals(self):
        if self.threshold > 0.5:
            self.red.on()
            print("red on")
        elif self.threshold > 0.3:
            self.yellow.on()
            print("yellow on")
        else:
            self.green.on()
            print("green on")
        sleep(2)
