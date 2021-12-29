import numpy as np
from human import *
from action import *
import os, shutil
from simulation_time import Time


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

time_simulation = Time()
foods = Foods().get_foods()         # List
humans = Humans(time_simulation).get_humans()      # List
actions = Actions().get_actions()   # Dict

SIMULATION_MAX = 15000
STEP = 1

humans[0].add_action(Action(Action.EAT, 30, impact=Properties(0, 0, 0, 0, 0, 0), size=100))

# for i in np.arange(3):
#     humans[0].add_action(Actions.actions[Action.WATCH_TV])
# for i in np.arange(150):
#     humans[0].add_action(Actions.actions[Action.READ])
# humans[0].add_action(Action(Action.RUN, steps=60, impact=Properties(-2.5, 0.005, 0.2, 0.005,  0.01, 0.01)))

# for i in np.arange(100):
#     humans[0].add_action(Action(Action.RUN, steps=60, impact=Properties(-10, 0.005, 0.2, 0.005,  0.01, 0.01)))

for i in np.arange(100):
    humans[0].add_action(Actions.actions[Action.READ])


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
    if _print: input()

