import numpy as np

from properties import Properties
from action import Action, Actions
import copy
import csv
import os


class Human:

    # CSV
    header = ["time", "weight", "height", "bmi", "liquid_absorbed", "liquid_waste", "solid_absorbed",
              "solid_waste", "plan", "current_action.name", "current_action.steps", "performance.motor_short",
              "performance.motor_long", "performance.cognitive_short", "performance.cognitive_long",
              "performance.cardio", "performance.regulatory", "energy.motor_short",
              "energy.motor_long", "energy.cognitive_short", "energy.cognitive_long",
              "energy.cardio", "energy.regulatory", "fatigue_level"]

    # Healthy issues
    COGNITIVE_FATIGUE = False
    MOTOR_FATIGUE = False
    CONGESTED = False
    URINE = False

    HUNGRY = False
    THIRSTY = False

    # Physiology - Configurable
    ABSORPTION_RATE_ENERGY = 0.4    # from energy to performance
    ABSORPTION_RATE_WATER = 1.5     # from energy to pee
    ABSORPTION_RATE_SOLID = 0.5     # from energy to poo
    BODY_REGULATION_RATE = 0.1      # normal body resources consumption

    LIQUID_RELEASE = 40             # thresholding for peeing
    SOLID_RELEASE = 40              # thresholding for pooing
    max_eat = 500

    # levels
    liquid_waste = 0                # bladder
    liquid_absorbed = 0             # energy
    solid_waste = 0                 # intestine
    solid_absorbed = 0              # energy

    THIRSTY_LEVEL = 10              # threshold to drink
    HUNGRY_LEVEL = 20               # threshold to eat

    fatigue = 1
    FATIGUE_RATE = 0.0009           # normal body fatigue during the day
    COGNITIVE_FATIGUE_LEVEL = 10    # threshold for tiredness - might result in resting actions
    MOTOR_FATIGUE_LEVEL = 10        # threshold for tiredness - might result in resting actions

    # Planning
    plan = []

    # TODO - DNA for later influence in major human characteristics
    def __init__(self, name="Neo", age=20, weight=70, height=1.7, performance=Properties(25, 50, 25, 50, 50, 50), energy=Properties(0, 0, 0, 0, 0, 0)):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.bmi = self.weight / self.height**2
        self.performance = performance
        self.energy = energy

        self.idle_action = Action(Action.IDLE, 1)
        self.current_action = self.idle_action

    def do_step(self):

        if self.current_action.name == Action.IDLE or self.current_action.steps == 1:
            if len(self.plan) > 0:
                self.current_action = copy.copy(self.get_next_action())
            else:
                self.current_action = self.idle_action
            return


        # human regulation
        if self.current_action.name == Action.EAT or self.current_action.name == Action.DRINK:
            self.update_energy(self.current_action)
        else:
            if self.current_action.name == Action.WC_PEE:
                self.liquid_waste = 0
            elif self.current_action.name == Action.WC_POO:
                self.liquid_waste = 0
                self.solid_waste = 0

            self.update_performance(self.current_action)
        self.consume_energy()
        self.regulation()

        self.current_action.steps = self.current_action.steps - 1

    # regulation of the plan
    def regulation(self):

        # Normal body resources consumption
        self.performance.motor_short = self.performance.motor_short - self.BODY_REGULATION_RATE / self.fatigue
        self.performance.cognitive_short = self.performance.cognitive_short - self.BODY_REGULATION_RATE / self.fatigue

        # Levels
        if self.liquid_waste > self.LIQUID_RELEASE and not self.action_in_plan(Action.WC_PEE):
            self.plan.insert(0, Actions.actions[Action.WC_PEE])
            self.URINE = True
        else:
            self.URINE = False
        if self.solid_waste > self.SOLID_RELEASE and not self.action_in_plan(Action.WC_POO):
            self.plan.insert(0, Actions.actions[Action.WC_POO])
            self.CONGESTED = True
        else:
            self.CONGESTED = False

        if self.performance.cognitive_short < 10:
            self.COGNITIVE_FATIGUE = True
        elif self.performance.cognitive_short > 30:
            self.COGNITIVE_FATIGUE = False

        if self.liquid_absorbed > self.THIRSTY_LEVEL:
            self.THIRSTY = False
        else:
            self.THIRSTY = True
        # if self.solid_absorbed > self.HUNGRY_LEVEL:
        if (self.performance.motor_short + self.performance.cognitive_short < 50):
            self.HUNGRY = True
        else:
            self.HUNGRY = False

        # Actions
        if self.COGNITIVE_FATIGUE:
            if not (False in [self.plan[i].cognitive_demanding for i in np.arange(len(self.plan))]):
                self.plan.insert(0, Actions.actions[Action.WATCH_TV])

        # Physiological needs are the priority so they go in the end in the code
        if self.THIRSTY and not self.action_in_plan(Action.DRINK) and not self.current_action.name == Action.DRINK:
            self.plan.insert(0, Actions.actions[Action.DRINK])
        if self.HUNGRY and not self.action_in_plan(Action.EAT) and not self.current_action.name == Action.EAT:
            self.plan.insert(0, Actions.actions[Action.EAT])



    # From eating to body
    def consume_energy(self):

        if self.liquid_absorbed <= 0: self.liquid_absorbed = 0
        else:
            self.liquid_waste = self.liquid_waste + self.ABSORPTION_RATE_WATER
            self.liquid_absorbed = self.liquid_absorbed - self.ABSORPTION_RATE_WATER
        if self.solid_absorbed <= 0: self.solid_absorbed = 0
        else:
            self.solid_waste = self.solid_waste + self.ABSORPTION_RATE_SOLID
            self.solid_absorbed = self.solid_absorbed - self.ABSORPTION_RATE_SOLID

        if self.energy.motor_short < 0: self.energy.motor_short = 0
        if self.energy.motor_long < 0: self.energy.motor_long = 0
        if self.energy.cognitive_short < 0: self.energy.cognitive_short = 0
        if self.energy.cognitive_long < 0: self.energy.cognitive_long = 0
        if self.energy.cardio < 0: self.energy.cardio = 0
        if self.energy.regulatory < 0: self.energy.regulatory = 0

        if self.energy.motor_short > 0:
            self.energy.motor_short = self.energy.motor_short - self.ABSORPTION_RATE_ENERGY
            if self.performance.motor_short < 0:
                self.weight = self.weight - self.ABSORPTION_RATE_ENERGY
            if self.performance.motor_short < 100:
                self.performance.motor_short = self.performance.motor_short + self.ABSORPTION_RATE_ENERGY
            else:
                self.weight = self.weight + self.ABSORPTION_RATE_ENERGY

        if self.energy.motor_long > 0:
            self.energy.motor_long = self.energy.motor_long - self.ABSORPTION_RATE_ENERGY
            if self.performance.motor_long < 0:
                self.weight = self.weight - self.ABSORPTION_RATE_ENERGY
            elif self.performance.motor_long < 100:
                self.performance.motor_long = self.performance.motor_long + self.ABSORPTION_RATE_ENERGY
            else:
                self.weight = self.weight + self.ABSORPTION_RATE_ENERGY

        if self.energy.cognitive_short > 0:
            self.energy.cognitive_short = self.energy.cognitive_short - self.ABSORPTION_RATE_ENERGY
            if self.performance.cognitive_short < 0:
                self.weight = self.weight - self.ABSORPTION_RATE_ENERGY
            elif self.performance.cognitive_short < 100:
                self.performance.cognitive_short = self.performance.cognitive_short + self.ABSORPTION_RATE_ENERGY
            else:
                self.weight = self.weight + self.ABSORPTION_RATE_ENERGY

        if self.energy.cognitive_long > 0:
            self.energy.cognitive_long = self.energy.cognitive_long - self.ABSORPTION_RATE_ENERGY
            if self.performance.cognitive_long < 0:
                self.weight = self.weight - self.ABSORPTION_RATE_ENERGY
            elif self.performance.cognitive_long < 100:
                self.performance.cognitive_long = self.performance.cognitive_long + self.ABSORPTION_RATE_ENERGY
            else:
                self.weight = self.weight + self.ABSORPTION_RATE_ENERGY

        if self.energy.cardio > 0:
            self.energy.cardio = self.energy.cardio - self.ABSORPTION_RATE_ENERGY
            if self.performance.cardio < 0:
                self.weight = self.weight - self.ABSORPTION_RATE_ENERGY
            elif self.performance.cardio < 100:
                self.performance.cardio = self.performance.cardio + self.ABSORPTION_RATE_ENERGY
            else:
                self.weight = self.weight + self.ABSORPTION_RATE_ENERGY

        if self.energy.regulatory > 0:
            self.energy.regulatory = self.energy.regulatory - self.ABSORPTION_RATE_ENERGY
            if self.performance.regulatory < 0:
                self.weight = self.weight - self.ABSORPTION_RATE_ENERGY
            elif self.performance.regulatory < 100:
                self.performance.regulatory = self.performance.regulatory + self.ABSORPTION_RATE_ENERGY
            else:
                self.weight = self.weight + self.ABSORPTION_RATE_ENERGY

        return None

    # when eating
    def update_energy(self, act):
        for f in act.foods:
            self.liquid_absorbed = self.liquid_absorbed + ((f.get_water()/act.steps) / len(act.foods))
            self.solid_absorbed = self.solid_absorbed + ((f.get_solid()/act.steps) / len(act.foods))

        for f in act.drinks:
            self.liquid_absorbed = self.liquid_absorbed + (f.get_water() / act.steps)
            self.solid_absorbed = self.solid_absorbed + (f.get_solid() / act.steps)

        self.energy.motor_short = self.energy.motor_short + (act.impact.motor_short/act.steps)
        self.energy.motor_long = self.energy.motor_long + (act.impact.motor_long/act.steps)
        self.energy.cognitive_short = self.energy.cognitive_short + (act.impact.cognitive_short/act.steps)
        self.energy.cognitive_long = self.energy.cognitive_long + (act.impact.cognitive_long/act.steps)
        self.energy.cardio = self.energy.cardio + (act.impact.cardio/act.steps)
        self.energy.regulatory = self.energy.regulatory + (act.impact.regulatory/act.steps)

    # when any action besides eating
    def update_performance(self, act):
        self.performance.motor_short = self.performance.motor_short + (act.impact.motor_short/act.steps)
        self.performance.motor_long = self.performance.motor_long + (act.impact.motor_long/act.steps)
        self.performance.cognitive_short = self.performance.cognitive_short + (act.impact.cognitive_short/act.steps)
        self.performance.cognitive_long = self.performance.cognitive_long + (act.impact.cognitive_long/act.steps)
        self.performance.cardio = self.performance.cardio + (act.impact.cardio/act.steps)
        self.performance.regulatory = self.performance.regulatory + (act.impact.regulatory/act.steps)

        self.fatigue = self.fatigue - self.FATIGUE_RATE

    def action_in_plan(self, act_name):
        for p in self.plan:
            if p.name == act_name:
                return True

        return False

    def add_action(self, action):
        self.plan.append(action)

    def get_next_action(self):
        res = self.plan[0]
        del self.plan[0]
        return res

    def add_physiological(self, action):
        self.plan.insert(0, action)

    def print_bmi(self):
        if self.bmi < 18.5: return "Underweight"
        elif self.bmi < 24.9: return "Normal weight"
        elif self.bmi < 29.9: return "Overweight"
        elif self.bmi < 34.9: return "Obesity Class I"
        elif self.bmi < 39.9: return "Obesity Class II"
        elif self.bmi > 40: return "Obesity Class III"
        else: return "None"

    def get_status(self):
        temp_status = []

        if self.FATIGUE: temp_status.append("Fatigue")
        if self.STRESS: temp_status.append("Stress")
        if self.HUNGRY: temp_status.append("Hungry")
        if self.THIRSTY: temp_status.append("Thirsty")
        if self.URINE: temp_status.append("Need to Urinate!")
        if self.CONGESTED: temp_status.append("Need to Poo!")

        if len(temp_status) == 0:
            return "Healthy"
        else:
            return temp_status

    def write_csv(self, folder, time_str):

        file = "{}{}.csv".format(folder, self.name)

        # open the file in the write mode
        f = open(file, 'a+')
        writer = csv.writer(f, delimiter=",", lineterminator='\n')

        # if file exists and is empty, remove existing and add header
        if os.stat(file).st_size == 0:
            writer.writerow(self.header)

        temp_plan = [p.name for p in self.plan]

        row_tuple = [time_str, round(self.weight, 2), round(self.height,2), round(self.bmi,2), round(self.liquid_absorbed,2), round(self.liquid_waste,2), round(self.solid_absorbed,2),
                 round(self.solid_waste,2), temp_plan, self.current_action.name, self.current_action.steps, round(self.performance.motor_short,2),
                 round(self.performance.motor_long,2), round(self.performance.cognitive_short,2), round(self.performance.cognitive_long,2),
                 round(self.performance.cardio,2), round(self.performance.regulatory,2), round(self.energy.motor_short,2),
                 round(self.energy.motor_long,2), round(self.energy.cognitive_short,2), round(self.energy.cognitive_long,2),
                 round(self.energy.cardio,2), round(self.energy.regulatory,2), self.fatigue]

        writer.writerow(row_tuple)
        f.close()

    def print(self):
        # Identity
        print("Name: ", self.name)
        print("Age: ", self.age)
        print("Weight:", self.weight)
        print("Height:", self.height)
        print("BMI:", self.print_bmi())
        print("Status: ", self.get_status())
        print("Fatigue: " , self.fatigue_level)

        # Physiology
        print("Liquid Absorbed: ", self.liquid_absorbed , "| Liquid Waste: ", self.liquid_waste)
        print("Solid Absorved: ", self.solid_absorbed, "| Solid Waste: ", self.solid_waste)

        if self.current_action.name == Action.EAT:
            f_names = [f.name for f in self.current_action.foods]
            print("Action: ", self.current_action.name, "Foods: ", f_names)
        elif self.current_action.name == Action.DRINK:
            f_names = [f.name for f in self.current_action.drinks]
            print("Action: ", self.current_action.name, "Drinks: ", f_names)
        else:
            print("Action: ", self.current_action.name)
        print("Step: ", self.current_action.steps)

        # Planning
        print("Plan:")
        for p in self.plan:
            if p.name == Action.EAT:
                f_names = [f.name for f in p.foods]
                print("\t", p.name, ":", p.steps, "mins - ", f_names)
            else:
                print("\t", p.name, ":", p.steps, "mins")

        print("Performance: ")
        self.performance.print()

        print("Energy: ")
        self.energy.print()


class Humans:

    humans = []

    # TODO - load all humans in csv file
    def __init__(self):

        self.humans.append(Human("Joao", 32, weight=85, height=1.89))
        # self.humans.append(Human("Sandra", 35))
        # self.humans.append(Human("Rui", 30))
        # self.humans.append(Human("Ste", 28))

    def get_humans(self):
        return self.humans
