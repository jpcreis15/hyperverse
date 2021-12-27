

class Properties:

    def __init__(self, motor_short=100, motor_long=100, cognitive_short=100, cognitive_long=100, cardio=100, regulatory=100):

        self.motor_short = motor_short
        self.motor_long = motor_long
        self.cognitive_short = cognitive_short
        self.cognitive_long = cognitive_long
        self.cardio = cardio
        self.regulatory = regulatory

    def print(self):
        print("\tMotor Short: ", self.motor_short)
        print("\tMotor Long: ", self.motor_long)
        print("\tCognitive Short: ", self.cognitive_short)
        print("\tCognitive Long: ", self.cognitive_long)
        print("\tCardio: ", self.cardio)
        print("\tRegulatory: ", self.regulatory)
