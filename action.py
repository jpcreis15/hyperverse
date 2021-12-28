from properties import Properties
from food import Foods
import random


class Action:

    RUN = "Run"
    WALK = "Walk"
    SIT_WORK = "Sit Work"
    READ = "Read"
    WATCH_TV = "Watch TV"
    SLEEP = "Sleep"
    IDLE = "Idle"

    EAT = "Eat"
    DRINK = "Drink"
    WC_PEE = "WC_PEE"
    WC_POO = "WC_POO"

    def __init__(self, name, steps, impact=Properties()):

        # Eat specific
        self.N_FOOD = 5
        self.foods = []
        self.drinks = []
        self.impact = impact
        self.name = name
        self.steps = steps
        self.cognitive_demanding = False
        self.motor_demanding = False

        if self.name == self.EAT:
            self.choose_food_update_impact()
        elif self.name == self.DRINK:
            self.choose_drink_update_impact()
        else:
            if impact.motor_short < 0: self.motor_demanding = True
            if impact.cognitive_short < 0: self.cognitive_demanding = True



    def print(self):
        print("Name: ", self.name)
        print("Duration: ", self.steps)
        print("Impact:")
        self.impact.print()

    def choose_food_update_impact(self):

        self.foods = [Foods.foods[i] for i in random.sample(range(0, len(Foods.foods)), self.N_FOOD)]

        for f in self.foods:
            self.impact.motor_short = self.impact.motor_short + f.weights.motor_short
            self.impact.motor_long = self.impact.motor_long + f.weights.motor_long
            self.impact.cognitive_short = self.impact.cognitive_short + f.weights.cognitive_short
            self.impact.cognitive_long = self.impact.cognitive_long + f.weights.cognitive_long
            self.impact.cardio = self.impact.cardio + f.weights.cardio
            self.impact.regulatory = self.impact.regulatory + f.weights.regulatory

    def choose_drink_update_impact(self):

        self.drinks = [Foods.drinks[random.randrange(len(Foods.drinks))]]

        for f in self.drinks:
            self.impact.motor_short = self.impact.motor_short + f.weights.motor_short
            self.impact.motor_long = self.impact.motor_long + f.weights.motor_long
            self.impact.cognitive_short = self.impact.cognitive_short + f.weights.cognitive_short
            self.impact.cognitive_long = self.impact.cognitive_long + f.weights.cognitive_long
            self.impact.cardio = self.impact.cardio + f.weights.cardio
            self.impact.regulatory = self.impact.regulatory + f.weights.regulatory



class Actions:

    actions = dict()

    def __init__(self):

        # TODO change to dictionary
        self.actions[Action.RUN] = Action(Action.RUN, 5, impact=Properties(-1, 0.3, 1, 0.3, 0.05, 0.05))
        self.actions[Action.WALK] = Action(Action.WALK, 5, impact=Properties(-0.3, 0.1, 0.3, 0.1, 0.02, 0.02))
        self.actions[Action.SIT_WORK] = Action(Action.SIT_WORK, 5, impact=Properties(0, -0.1, -0.3, 0.1, -0.01, -0.01))
        self.actions[Action.READ] = Action(Action.READ, 30, impact=Properties(-0.5, -0.1, -2.5, 0.5, -0.01, -0.01))
        self.actions[Action.WATCH_TV] = Action(Action.WATCH_TV, 30, impact=Properties(0.5, -0.1, 0.5, -0.1, -0.05, -0.05))
        self.actions[Action.SLEEP] = Action(Action.SLEEP, 60, impact=Properties(-0.05, 0.1, 0.2, 0.1, 0.05, 0.05))

        # Physiology regulation
        self.actions[Action.EAT] = Action(Action.EAT, 30, impact=Properties(0, 0, 0, 0, 0, 0))
        self.actions[Action.DRINK] = Action(Action.DRINK, 2, impact=Properties(0, 0, 0, 0, 0, 0))
        self.actions[Action.WC_PEE] = Action(Action.WC_PEE, 2, impact=Properties(0, 0, 0, 0, 0, 0))
        self.actions[Action.WC_POO] = Action(Action.WC_POO, 10, impact=Properties(0, 0, 0, 0, 0, 0))

    def get_actions(self):
        return self.actions
