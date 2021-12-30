import time
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

SIMULATION_MAX = 100000
STEP = 1

humans[0].add_action(Action(Action.EAT, 30, impact=Properties(0, 0, 0, 0, 0, 0), size=100))

# for i in np.arange(3):
#     humans[0].add_action(Actions.actions[Action.WATCH_TV])
# for i in np.arange(150):
#     humans[0].add_action(Actions.actions[Action.READ])
# humans[0].add_action(Action(Action.RUN, steps=60, impact=Properties(-2.5, 0.005, 0.2, 0.005,  0.01, 0.01)))

for i in np.arange(600):
    humans[0].add_action(Action(Action.RUN, steps=60, impact=Properties(-10, 0.005, 0.2, 0.005,  0.01, 0.01)))

    for j in np.arange(8):
        humans[0].add_action(Actions.actions[Action.READ])

    for j in np.arange(8):
        humans[0].add_action(Actions.actions[Action.WATCH_TV])


#######################################################################################

_print = False
folder = "results/"
remove_all_files(folder)

point = 20
val = SIMULATION_MAX/point

start = time.time()
for tick in np.arange(SIMULATION_MAX):

    if (tick % val) == 0:
        num = (tick / val)
        print("[", '='*int(num), " "*(int(point - num) - 1), "] ", round((tick/SIMULATION_MAX)*100,2) , "%")

    # Simulation step
    if _print: time_simulation.print()
    time_simulation.do_step(STEP)

    # Human step
    humans[0].do_step()
    if _print: humans[0].print()
    #humans[0].write_csv_light(folder, time_simulation.str())

    if _print: print('=~'*20)
    if _print: input()

end = time.time()
seconds = end - start
minutes = seconds/60
hours = minutes/60
print("Simulation time (hours): {}h {}min {}sec".format(int(hours), int(minutes), int(seconds)-(int(minutes)*60)))