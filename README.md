# Hyperverse

Personal project about the Hyperverse. Similar to the Metaverse, but better, because Hyper is always better than Meta.

Main implemented classes:

- simulation_time.py - Simple Class that implements time passing by. 
- properties.py
  - Properties - Human properties that will be used by Actions.
    - motor_short - Short-term motor capability - e.g., used for immediate running actions
    - motor_long - Long-term motor capability - e.g., used for better long term running performance
    - cognitive_short - Short-term cognitive capability - e.g., used for immediate reading actions
    - cognitive_long - Long-term cognitive capability - e.g., used for better action performance like reading more pages for the same amount of time
    - cardio - Cardiovascular factor that helps in motor activities
    - regulatory - Regulatory and immune system that manages all the organisms thresholds and rates, e.g., speed of absorption
- food.py
  - Nutrition
    - poli_fat - Polyunsaturated Fats
    - satu_fat = Saturated Fats
    - carbs = Carbohydrates
    - sugar = Sugars
    - protein = Protein
    - vitamins = Vitamins
    - fibers = Fibers 
  - Food - Main variables are:
    - nutrition - "Nutrition" values for food, e.g. fibers, protein, sugars, etc.
    - weights - Weights are "Properties". Basically, the idea is to convert the nutritional values of food into human properties, such as motor short and long, cognitive short and long, cardio and regulatory
    - water_percentage - Percentage of water in food
  - Foods - Collection of all foods and drinks. This Class will be used to load all foods and drink from CSV files.
    - foods - List of all foods
    - drinks - List of all drinks
- action.py
  - Action - For simplicity reasons, Action is shared among physiological and ordinary actions, like eating, drink, peeing, running, reading and sleeping.
    - self.N_FOOD - (Eat specific) Default to 5. When eating, chooses among 5 possible available foods. 
    - self.foods - (Eat specific) List with all foods
    - self.drinks - (Drink specific) List with all drinks
    - self.impact - Importance of the action for human "Properties". If physiologic actions it impacts the "Energy" values from humans. If ordinary task, it impacts the "Performance" values of humans.
    - self.size - (Eat specific) - size in mg of the food to be eaten
    - self.baseline_size - (Eat specific) Default to 100. Amount of food considered in the nutritional table values.
    - self.name - Action name
    - self.steps - How many tick / steps this action should take
    - self.cognitive_demanding - Default to False. Know a priori if the task is cognitive demanding or not. If it impacts negatively the human property of "cognitive_short" such as reading, then it is cognitive demanding   
    - self.motor_demanding - Default to False. Know a priori if the task is motor demanding or not. If it impacts negatively the human property of "motor_short" such as running, then it is motor demanding 
  - Actions - Collection of all actions. This Class will be used to load all actions from CSV files.
    - actions - List of all actions.
- human.py
  - Human
    - name - Name
    - age - Age
    - height - Height
    - weight - Weight
    - bmi - Body Mass Index following the eqation (self.weight / self.height**2)
    - performance - "Properties" object that will be consumed by Actions.
    - energy - "Properties" object that is fed by food and absorbed into "performance" object. 
    - simul_time - Simulation time 
    - idle_action - Default Idle action that is used when the human has nothing more to do. 
    - current_action - Current action is execution.
  - Humans - Collection of all humans. This Class will be used to load all humans from a CSV file.
    - humans - List of all humans


The central idea is that food, through its nutrition values, is converted into human energy "Properties" (simulating stomach and intestines). Thus, these energy "Properties" will be absorbed into the body as human performance "Properties" to be consumed by actions. Since each action directly impacts these "Properties", the execution of these actions will decrease the available reserves of human performance "Properties". Then, is through the variation of such human performance "Properties" that characteristics such as weight will vary during time.     