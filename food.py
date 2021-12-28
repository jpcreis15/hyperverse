from human import Properties


class Nutrition:

    def __init__(self, poli_fat=0.0, satu_fat=0.0, carbs=0.0, sugar=0.0, protein=0.0, vitamins=0.0, fibers=0.0):

        self.poli_fat = poli_fat
        self.satu_fat = satu_fat
        self.carbs = carbs
        self.sugar = sugar
        self.protein = protein
        self.vitamins = vitamins
        self.fibers = fibers

    def print(self):
        print("\tPoli Fat: ", self.poli_fat)
        print("\tSaturated Fat: ", self.satu_fat)
        print("\tCarbs: ", self.carbs)
        print("\tSugar: ", self.sugar)
        print("\tProtein: ", self.protein)
        print("\tVitamins: ", self.vitamins)
        print("\tFibers: ", self.fibers)


class Food:

    def __init__(self, name, type, nutrition=Nutrition(), water_percentage=0.5):

        self.type = type
        self.name = name

        self.nutrition = nutrition
        self.weights = self.get_weights()
        self.water_percentage = water_percentage

    def get_weights(self):

        temp_motor_short = (self.nutrition.carbs / 2.5) + (self.nutrition.sugar / 2.5)
        temp_motor_long = self.nutrition.protein / 2.5
        temp_cognitive_short = (self.nutrition.carbs / 2.5) + (self.nutrition.sugar / 2.5)
        temp_cognitive_long = (self.nutrition.poli_fat / 2.5) + (self.nutrition.vitamins / 2.5)

        temp_cardio = (self.nutrition.vitamins / 2.5) + (self.nutrition.poli_fat / 2.5)
        temp_regulatory = (self.nutrition.vitamins / 2.5)

        return Properties(temp_motor_short, temp_motor_long, temp_cognitive_short, temp_cognitive_long, temp_cardio, temp_regulatory)

    def get_nutrition_weight(self):
        return self.nutrition.poli_fat + self.nutrition.satu_fat + self.nutrition.carbs + self.nutrition.sugar + self.nutrition.protein + self.nutrition.vitamins + self.nutrition.fibers

    def get_water(self):
        return (100 - self.get_nutrition_weight()) * self.water_percentage

    def get_solid(self):
        return (100 - self.get_nutrition_weight()) * (1 - self.water_percentage)

    def print(self):

        print("Name: ", self.name)
        print("Type: ", self.type)

        print("Nutrition: ")
        self.nutrition.print()

        print("Weights: ")
        self.weights.print()

class Foods:

    foods = []
    drinks = []

    # TODO - load all foods from a csv file
    def __init__(self):

        # Foods
        self.foods.append(Food("Potato", "tuber", nutrition=Nutrition(0.1, 0, 17, 0.2, 2, 0, 2.2), water_percentage=0.2))
        self.foods.append(Food("Rice", "tuber", nutrition=Nutrition(0.1, 0, 57, 0.2, 2, 0, 2.2), water_percentage=0.2))
        self.foods.append(Food("Pasta", "tuber", nutrition=Nutrition(0.9, 0.2, 25, 0, 5, 0.2, 0), water_percentage=0.2))

        self.foods.append(Food("Cake", "pastery", nutrition=Nutrition(18, 6, 48, 15, 2, 0, 2), water_percentage=0.1))

        self.foods.append(Food("Beef", "meat", nutrition=Nutrition(9, 6, 0, 0, 26, 0, 0), water_percentage=0.3))
        self.foods.append(Food("Chicken", "meat", nutrition=Nutrition(10.2, 3.8, 0, 0, 27, 0.4, 0), water_percentage=0.3))
        self.foods.append(Food("Turkey", "meat", nutrition=Nutrition(4.8, 2.2, 0.1, 0, 29, 0.4, 0), water_percentage=0.3))
        self.foods.append(Food("Pork", "meat", nutrition=Nutrition(9, 5, 0, 0, 27, 0.5, 0), water_percentage=0.3))

        self.foods.append(Food("Lettuce", "vegetables", nutrition=Nutrition(0.2, 0, 0.8, 0.8, 1.4, 0.1, 1.3), water_percentage=0.5))
        self.foods.append(Food("Tomato", "vegetables", nutrition=Nutrition(0.2, 0, 3.9, 2.6, 0.9, 0.1, 1.2), water_percentage=0.95))

        # Drinks
        self.drinks.append(Food("Water", "drink", nutrition=Nutrition(0, 0, 0, 0, 0, 0.1, 0.1), water_percentage=1))

    def get_foods(self):
        return self.foods
