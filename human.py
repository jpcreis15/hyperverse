import numpy as np

from properties import Properties
from action import Action, Actions
from simulation_time import Time
import copy
import csv
import os


class Human:

    # CSV
    header = ["time", "weight", "height", "bmi", "liquid_absorbed", "liquid_waste", "solid_absorbed",
              "solid_waste", "plan_physio", "plan", "current_action.name", "current_action.steps", "performance.motor_short",
              "performance.motor_long", "performance.cognitive_short", "performance.cognitive_long",
              "performance.cardio", "performance.regulatory", "energy.motor_short",
              "energy.motor_long", "energy.cognitive_short", "energy.cognitive_long",
              "energy.cardio", "energy.regulatory", "fatigue_level", "MOTOR_FATIGUE", "COGNITIVE_FATIGUE"]

    header_light = ["time", "weight", "plan_physio", "current_action.name", "current_action.steps", "performance.motor_short",
              "performance.motor_long", "performance.cognitive_short", "performance.cognitive_long",
              "performance.cardio", "performance.regulatory", "energy.motor_short",
              "energy.motor_long", "energy.cognitive_short", "energy.cognitive_long", "fatigue", "MOTOR_FATIGUE", "COGNITIVE_FATIGUE"]

    # Healthy issues
    COGNITIVE_FATIGUE = False
    MOTOR_FATIGUE = False
    CONGESTED = False
    URINE = False
    SLEEP = False

    HUNGRY = False
    THIRSTY = False

    # Physiology - Configurable
    ABSORPTION_RATE_ENERGY_SHORT = 0.2    # from energy to performance
    ABSORPTION_RATE_ENERGY_LONG = 0.002    # from energy to performance
    ABSORPTION_RATE_WATER = 1.5     # from energy to pee
    ABSORPTION_RATE_SOLID = 0.5     # from energy to poo
    ABSORPTION_RATE_WEIGHT = 0.001  # from surplus of motor to weight
    BODY_REGULATION_RATE = 0.1      # normal body resources consumption

    LIQUID_RELEASE = 80             # thresholding for peeing
    SOLID_RELEASE = 80              # thresholding for pooing
    max_eat = 500

    # levels
    liquid_waste = 0                # bladder
    liquid_absorbed = 0             # energy
    solid_waste = 0                 # intestine
    solid_absorbed = 0              # energy

    THIRSTY_LEVEL = 10              # threshold to drink
    HUNGRY_LEVEL = 20               # threshold to eat

    fatigue = 1
    FATIGUE_RATE = 0.0011           # normal body fatigue during the day
    COGNITIVE_FATIGUE_LEVEL = 10    # threshold for tiredness - might result in resting actions
    COGNITIVE_NORMAL_LEVEL = 30     # threshold for tiredness - might result in resting actions
    MOTOR_FATIGUE_LEVEL = 10        # threshold for tiredness - might result in resting actions
    MOTOR_NORMAL_LEVEL = 30         # threshold for tiredness - might result in resting actions

    schedule_lunch = [12, 14]
    schedule_dinner = [19, 21]
    BED_TIME = [22, 2]

    # Planning
    plan = []
    plan_physio = []
    SHORT_TERM_PLAN = 2

    # TODO - DNA for later influence in major human characteristics
    def __init__(self, simul_time, name="Neo", age=20, weight=70, height=1.7, performance=Properties(50, 50, 50, 50, 50, 50), energy=Properties(0, 0, 0, 0, 0, 0)):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.bmi = self.weight / self.height**2
        self.performance = performance
        self.energy = energy
        self.simul_time = simul_time

        self.idle_action = Action(Action.IDLE, 1)
        self.current_action = self.idle_action

    def do_step(self):

        if self.current_action.name == Action.IDLE or self.current_action.steps == 1:
            if len(self.plan_physio) > 0:
                self.current_action = copy.copy(self.get_next_action(self.plan_physio))
            elif len(self.plan) > 0:
                self.current_action = copy.copy(self.get_next_action(self.plan))
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

        # if self.performance.motor_short < 0: self.performance.motor_short = 0
        # if self.performance.motor_long < 0: self.performance.motor_long = 0
        # if self.performance.cognitive_short < 0: self.performance.cognitive_short = 0
        # if self.performance.cognitive_long < 0: self.performance.cognitive_long = 0
        # if self.performance.cardio < 0: self.performance.cardio = 0
        # if self.performance.regulatory < 0: self.performance.regulatory = 0
        if self.performance.motor_short > 100: self.performance.motor_short = 100
        if self.performance.motor_long > 100: self.performance.motor_long = 100
        if self.performance.cognitive_short > 100: self.performance.cognitive_short = 100
        if self.performance.cognitive_long > 100: self.performance.cognitive_long = 100
        if self.performance.cardio > 100: self.performance.cardio = 100
        if self.performance.regulatory > 100: self.performance.regulatory = 100

        if self.energy.motor_short < 0: self.energy.motor_short = 0
        if self.energy.motor_long < 0: self.energy.motor_long = 0
        if self.energy.cognitive_short < 0: self.energy.cognitive_short = 0
        if self.energy.cognitive_long < 0: self.energy.cognitive_long = 0
        if self.energy.cardio < 0: self.energy.cardio = 0
        if self.energy.regulatory < 0: self.energy.regulatory = 0

        self.current_action.steps = self.current_action.steps - 1

    # regulation of the plan
    def regulation(self):

        ################################################################
        # Arquetypes of the system. Learning should bot be made here
        # Normal body resources consumption
        if self.current_action.name == Action.SLEEP:
            self.fatigue = 1
        else:
            factor = self.BODY_REGULATION_RATE / self.fatigue
            self.performance.motor_short = self.performance.motor_short - factor
            self.performance.cognitive_short = self.performance.cognitive_short - factor

        # Levels
        if (self.fatigue < 0.3 and self.simul_time.hour >= self.BED_TIME[0]) or (self.fatigue < 0.3 and self.simul_time.hour <= self.BED_TIME[1]) and not self.action_in_plan(Action.SLEEP, self.plan_physio):
            self.SLEEP = True
        else:
            self.SLEEP = False

        if self.liquid_waste > self.LIQUID_RELEASE and not self.action_in_plan(Action.WC_PEE, self.plan_physio):
            # self.plan.insert(0, Actions.actions[Action_Physiologic.WC_PEE])
            self.plan_physio.insert(0, Actions.actions[Action.WC_PEE])
            self.URINE = True
        else:
            self.URINE = False
        if self.solid_waste > self.SOLID_RELEASE and not self.action_in_plan(Action.WC_POO, self.plan_physio):
            # self.plan.insert(0, Actions.actions[Action_Physiologic.WC_POO])
            self.plan_physio.insert(0, Actions.actions[Action.WC_POO])
            self.CONGESTED = True
        else:
            self.CONGESTED = False

        if self.performance.cognitive_short < self.COGNITIVE_FATIGUE_LEVEL:
            self.COGNITIVE_FATIGUE = True
        elif self.performance.cognitive_short > self.COGNITIVE_NORMAL_LEVEL:
            self.COGNITIVE_FATIGUE = False

        if self.performance.motor_short < self.MOTOR_FATIGUE_LEVEL:
            self.MOTOR_FATIGUE = True
        elif self.performance.motor_short > self.MOTOR_NORMAL_LEVEL:
            self.MOTOR_FATIGUE = False

        if self.liquid_absorbed > self.THIRSTY_LEVEL:
            self.THIRSTY = False
        else:
            self.THIRSTY = True
        # if self.solid_absorbed > self.HUNGRY_LEVEL:
        # if (self.performance.motor_short + self.performance.cognitive_short < 50):
        if (self.energy.motor_short + self.energy.motor_long + self.energy.cognitive_short + self.energy.cognitive_long + self.energy.cardio + self.energy.regulatory) < 10:
            self.HUNGRY = True
        else:
            self.HUNGRY = False

        #############################################################################
        # Location to implement learning
        # Actions
        temp_len = self.SHORT_TERM_PLAN
        if len(self.plan) < self.SHORT_TERM_PLAN: temp_len = len(self.plan)
        if self.COGNITIVE_FATIGUE:
            # if not (False in [self.plan[i].cognitive_demanding for i in np.arange(len(self.plan[0:temp_len]))]) and self.current_action.cognitive_demanding:
            if self.current_action.cognitive_demanding:
                self.plan.insert(0, Actions.actions[Action.WATCH_TV])
                self.current_action.steps = 2   # Needs to be 2 because right after regulation steps are decreased
        if self.MOTOR_FATIGUE:
            # if not (False in [self.plan[i].motor_demanding for i in np.arange(len(self.plan[0:temp_len]))]) and self.current_action.motor_demanding:
            if self.current_action.motor_demanding:
                self.plan.insert(0, Actions.actions[Action.WATCH_TV])
                self.current_action.steps = 2  # Needs to be 2 because right after regulation steps are decreased


        # Physiological needs are the priority so they go in the end in the code
        if self.THIRSTY and not self.action_in_plan(Action.DRINK, self.plan_physio) and not self.current_action.name == Action.DRINK:
            # Give priority to sleep
            # TODO change this for a insert_physio function to avoid changing in all list inserts
            if Action.SLEEP in self.plan_physio:
                self.plan_physio.insert(1, Actions.actions[Action.DRINK])
            else:
                self.plan_physio.insert(0, Actions.actions[Action.DRINK])

        if self.HUNGRY and not self.action_in_plan(Action.EAT, self.plan_physio) and not self.current_action.name == Action.EAT:
            if (self.schedule_lunch[0] <= self.simul_time.hour <= self.schedule_lunch[1]) \
                    or (self.schedule_dinner[0] <= self.simul_time.hour <= self.schedule_dinner[1]):
                if Action.SLEEP in self.plan_physio:
                    self.plan_physio.insert(1, Action(Action.EAT, 30, impact=Properties(0, 0, 0, 0, 0, 0), size=250))
                else:
                    self.plan_physio.insert(0, Action(Action.EAT, 30, impact=Properties(0, 0, 0, 0, 0, 0), size=250))
            else:
                if Action.SLEEP in self.plan_physio:
                    self.plan_physio.insert(1, Action(Action.EAT, 30, impact=Properties(0, 0, 0, 0, 0, 0), size=100))
                else:
                    self.plan_physio.insert(0, Action(Action.EAT, 30, impact=Properties(0, 0, 0, 0, 0, 0), size=100))

        if self.SLEEP and not self.action_in_plan(Action.SLEEP, self.plan_physio) and not self.current_action.name == Action.SLEEP:
            self.plan_physio.insert(0, Actions.actions[Action.SLEEP])


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

        if self.energy.motor_short > 0:
            self.energy.motor_short = self.energy.motor_short - self.ABSORPTION_RATE_ENERGY_SHORT
            self.performance.motor_short = self.performance.motor_short + self.ABSORPTION_RATE_ENERGY_SHORT

        if self.performance.motor_short <= 0:
            self.weight = self.weight - (self.ABSORPTION_RATE_ENERGY_SHORT * self.ABSORPTION_RATE_WEIGHT)
        if self.performance.motor_short >= 100:
            self.weight = self.weight + (self.ABSORPTION_RATE_ENERGY_SHORT * self.ABSORPTION_RATE_WEIGHT)

        # if self.energy.motor_long > 0:
        #     self.energy.motor_long = self.energy.motor_long - self.ABSORPTION_RATE_ENERGY
        #     if self.performance.motor_long < 0:
        #         self.weight = self.weight - (self.ABSORPTION_RATE_ENERGY  * 0.1)
        #     elif self.performance.motor_long < 100:
        #         self.performance.motor_long = self.performance.motor_long + self.ABSORPTION_RATE_ENERGY
        #     else:
        #         self.weight = self.weight + (self.ABSORPTION_RATE_ENERGY * 0.1)

        if self.energy.motor_long > 0:
            self.energy.motor_long = self.energy.motor_long - self.ABSORPTION_RATE_ENERGY_SHORT
            self.performance.motor_long = self.performance.motor_long + self.ABSORPTION_RATE_ENERGY_LONG
            
        if self.energy.cognitive_short > 0:
            self.energy.cognitive_short = self.energy.cognitive_short - self.ABSORPTION_RATE_ENERGY_SHORT
            self.performance.cognitive_short = self.performance.cognitive_short + self.ABSORPTION_RATE_ENERGY_SHORT

        if self.performance.cognitive_short <= 0:
            self.weight = self.weight - (self.ABSORPTION_RATE_ENERGY_SHORT * self.ABSORPTION_RATE_WEIGHT)
        # if self.performance.cognitive_short >= 100:
        #     self.weight = self.weight + (self.ABSORPTION_RATE_ENERGY_SHORT * self.ABSORPTION_RATE_WEIGHT)

        # if self.energy.cognitive_long > 0:
        #     self.energy.cognitive_long = self.energy.cognitive_long - self.ABSORPTION_RATE_ENERGY
        #     if self.performance.cognitive_long < 0:
        #         self.weight = self.weight - (self.ABSORPTION_RATE_ENERGY * 0.1)
        #     elif self.performance.cognitive_long < 100:
        #         self.performance.cognitive_long = self.performance.cognitive_long + self.ABSORPTION_RATE_ENERGY
        #     else:
        #         self.weight = self.weight + (self.ABSORPTION_RATE_ENERGY * 0.1)

        if self.energy.cognitive_long > 0:
            self.energy.cognitive_long = self.energy.cognitive_long - self.ABSORPTION_RATE_ENERGY_SHORT
            self.performance.cognitive_long = self.performance.cognitive_long + self.ABSORPTION_RATE_ENERGY_LONG

        # if self.energy.cardio > 0:
        #     self.energy.cardio = self.energy.cardio - self.ABSORPTION_RATE_ENERGY
        #     if self.performance.cardio < 0:
        #         self.weight = self.weight - (self.ABSORPTION_RATE_ENERGY * 0.1)
        #     elif self.performance.cardio < 100:
        #         self.performance.cardio = self.performance.cardio + self.ABSORPTION_RATE_ENERGY
        #     else:
        #         self.weight = self.weight + (self.ABSORPTION_RATE_ENERGY * 0.1)

        if self.energy.cardio > 0:
            self.energy.cardio = self.energy.cardio - self.ABSORPTION_RATE_ENERGY_SHORT
            self.performance.cardio = self.performance.cardio + self.ABSORPTION_RATE_ENERGY_LONG

        # if self.energy.regulatory > 0:
        #     self.energy.regulatory = self.energy.regulatory - self.ABSORPTION_RATE_ENERGY
        #     if self.performance.regulatory < 0:
        #         self.weight = self.weight - (self.ABSORPTION_RATE_ENERGY * 0.1)
        #     elif self.performance.regulatory < 100:
        #         self.performance.regulatory = self.performance.regulatory + self.ABSORPTION_RATE_ENERGY
        #     else:
        #         self.weight = self.weight + (self.ABSORPTION_RATE_ENERGY * 0.1)
        if self.energy.regulatory > 0:
            self.energy.regulatory = self.energy.regulatory - self.ABSORPTION_RATE_ENERGY_SHORT
            self.performance.regulatory = self.performance.regulatory + self.ABSORPTION_RATE_ENERGY_LONG



        return None

    # when eating
    def update_energy(self, act):

        reduction_factor = 0.2

        for f in act.foods:
            self.liquid_absorbed = self.liquid_absorbed + (((f.get_water()/act.steps) / len(act.foods)) * reduction_factor)
            self.solid_absorbed = self.solid_absorbed + (((f.get_solid()/act.steps) / len(act.foods)) * reduction_factor)

        for f in act.drinks:
            self.liquid_absorbed = self.liquid_absorbed + ((f.get_water() / act.steps) * reduction_factor)
            self.solid_absorbed = self.solid_absorbed + ((f.get_solid() / act.steps) * reduction_factor)

        self.energy.motor_short = self.energy.motor_short + (act.impact.motor_short/act.steps)
        self.energy.motor_long = self.energy.motor_long + (act.impact.motor_long/act.steps)
        self.energy.cognitive_short = self.energy.cognitive_short + (act.impact.cognitive_short/act.steps)
        self.energy.cognitive_long = self.energy.cognitive_long + (act.impact.cognitive_long/act.steps)
        self.energy.cardio = self.energy.cardio + (act.impact.cardio/act.steps)
        self.energy.regulatory = self.energy.regulatory + (act.impact.regulatory/act.steps)

        if self.energy.motor_short < 0: self.energy.motor_short = 0
        if self.energy.motor_long < 0: self.energy.motor_long = 0
        if self.energy.cognitive_short < 0: self.energy.cognitive_short = 0
        if self.energy.cognitive_long < 0: self.energy.cognitive_long = 0
        if self.energy.cardio < 0: self.energy.cardio = 0
        if self.energy.regulatory < 0: self.energy.regulatory = 0

    # when any action besides eating
    def update_performance(self, act):
        self.performance.motor_short = self.performance.motor_short + (act.impact.motor_short/act.steps)
        self.performance.motor_long = self.performance.motor_long + (act.impact.motor_long/act.steps)
        self.performance.cognitive_short = self.performance.cognitive_short + (act.impact.cognitive_short/act.steps)
        self.performance.cognitive_long = self.performance.cognitive_long + (act.impact.cognitive_long/act.steps)
        self.performance.cardio = self.performance.cardio + (act.impact.cardio/act.steps)
        self.performance.regulatory = self.performance.regulatory + (act.impact.regulatory/act.steps)

        self.fatigue = self.fatigue - self.FATIGUE_RATE

    def action_in_plan(self, act_name, plan):
        for p in plan:
            if p.name == act_name:
                return True

        return False

    def add_action(self, action):
        self.plan.append(action)

    def get_next_action(self, plan):
        res = plan[0]
        del plan[0]
        return res

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

        if self.COGNITIVE_FATIGUE: temp_status.append("Cognitive Fatigue")
        if self.MOTOR_FATIGUE: temp_status.append("Motor Fatigue")
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

        temp_plan = [p.name for p in self.plan[0:10]]
        temp_plan_physio = [p.name for p in self.plan_physio[0:10]]

        row_tuple = [time_str, round(self.weight, 2), round(self.height,2), round(self.bmi,2), round(self.liquid_absorbed,2), round(self.liquid_waste,2), round(self.solid_absorbed,2),
                 round(self.solid_waste,2), temp_plan_physio, temp_plan, self.current_action.name, self.current_action.steps, round(self.performance.motor_short,2),
                 round(self.performance.motor_long,2), round(self.performance.cognitive_short,2), round(self.performance.cognitive_long,2),
                 round(self.performance.cardio,2), round(self.performance.regulatory,2), round(self.energy.motor_short,2),
                 round(self.energy.motor_long,2), round(self.energy.cognitive_short,2), round(self.energy.cognitive_long,2),
                 round(self.energy.cardio,2), round(self.energy.regulatory,2), self.fatigue, self.MOTOR_FATIGUE, self.COGNITIVE_FATIGUE]

        writer.writerow(row_tuple)
        f.close()

    def write_csv_light(self, folder, time_str):

        file = "{}{}_light.csv".format(folder, self.name)

        # open the file in the write mode
        f = open(file, 'a+')
        writer = csv.writer(f, delimiter=",", lineterminator='\n')

        # if file exists and is empty, remove existing and add header
        if os.stat(file).st_size == 0:
            writer.writerow(self.header_light)

        row_tuple = [time_str, round(self.weight, 2), [p.name for p in self.plan_physio[0:10]], self.current_action.name, self.current_action.steps, round(self.performance.motor_short,2),
                 round(self.performance.motor_long,2), round(self.performance.cognitive_short,2), round(self.performance.cognitive_long,2),
                 round(self.performance.cardio,2), round(self.performance.regulatory,2), round(self.energy.motor_short,2),
                 round(self.energy.motor_long,2), round(self.energy.cognitive_short,2), round(self.energy.cognitive_long,2), self.fatigue, self.MOTOR_FATIGUE, self.COGNITIVE_FATIGUE]

        writer.writerow(row_tuple)
        f.close()

    def print(self):
        # Identity
        print("Time: ", self.simul_time.str())
        print("Name: ", self.name)
        print("Age: ", self.age)
        print("Weight:", self.weight)
        print("Height:", self.height)
        print("BMI:", self.print_bmi())
        print("Status: ", self.get_status())
        print("Fatigue: " , self.fatigue)

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
        for p in self.plan[0:10]:
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
    def __init__(self, time_simulation):

        self.humans.append(Human(simul_time=time_simulation, name="Joao", age=32, weight=85, height=1.89))

    def get_humans(self):
        return self.humans
