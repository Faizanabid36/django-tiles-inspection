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
            self.yellow.off()
            self.green.off()
            print("red on")
        elif self.threshold > 0.3:
            self.yellow.on()
            self.green.off()
            self.red.off()
            print("yellow on")
        else:
            self.green.on()
            self.yellow.off()
            self.red.off()
            print("green on")