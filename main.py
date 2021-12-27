import numpy as np
from human import *
from action import *
import os, shutil


class Time:

    def __init__(self):

        self.day = 1
        self.month = 1
        self.year = 2020
        self.time = 480

        self.max_time = 1440
        self.max_day = 30
        self.max_month = 12

    def print(self):
        hour_temp = self.time//60
        minute_temp = self.time - (hour_temp*60)
        print("{0}:{1} {2}/{3}/{4}".format(hour_temp, minute_temp, self.day, self.month, self.year))

    def str(self):
        hour_temp = self.time // 60
        minute_temp = self.time - (hour_temp * 60)
        return "{}/{}/{} {}:{}:00".format(self.day, self.month, self.year, hour_temp, minute_temp)

    def do_step(self, i):
        self.time = self.time + 1
        if self.time > self.max_time:
            self.day = self.day + 1
            self.time = 1
            if self.day > self.max_day:
                self.month = self.month + 1
                self.day = 1
                if self.month > self.max_month:
                    self.year = self.year + 1

def remove_all_files(folder):

    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


foods = Foods().get_foods()         # List
humans = Humans().get_humans()      # List
actions = Actions().get_actions()   # Dict
time_simulation = Time()

# actions[Action.RUN].print()
# humans[0].print()
# foods[2].print()

SIMULATION_MAX = 5000
STEP = 1

humans[0].add_action(Actions.actions[Action.EAT])
# humans[0].add_action(Actions.actions[Action.SLEEP])
# humans[0].add_action(Actions.actions[Action.WC])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])
humans[0].add_action(Actions.actions[Action.WATCH_TV])

#######################################################################################

_print = False
folder = "results/"
remove_all_files(folder)

for tick in np.arange(SIMULATION_MAX):

    # Simulation step
    if _print: time_simulation.print()
    time_simulation.do_step(STEP)

    # Human step
    humans[0].do_step()
    if _print: humans[0].print()
    humans[0].write_csv(folder, time_simulation.str())

    if _print: print('=~'*20)
    #input()

