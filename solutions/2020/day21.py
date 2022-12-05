from utils.abstract import FileReaderSolution
from typing import Dict, List
from enum import Enum
import math

class Food:
    allergens = List[str]
    ingredients = List[str]

    def __init__(self, input_str):
        parts = input_str.split(" (")

        self.allergens = parts[0].split(" ")

        self.ingredients = [x.replace("contains ", '').strip() for x in parts[1].strip(')').split(',')]

    def __str__(self):
        return " ".join(self.allergens) + "(contains " + " ".join(self.ingredients) + ")"


class Day21:
    foods: List[Food] = []

    def parse_input(self, input_data: str):
        for line in input_data.splitlines():
            self.foods.append(Food(line))

    def remove_ingredients(self, allergen, ingredient):
        for food in self.foods:
            if allergen in food.allergens:
                food.allergens.remove(allergen)

            if ingredient in food.ingredients:
                food.ingredients.remove(ingredient)


class Day21PartA(Day21, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)
        allergens = {}
        all_allergens =  list(set([item for sublist in self.foods for item in sublist.allergens]))
        all_ingredients = list(set([item for sublist in self.foods for item in sublist.ingredients]))

        for allergen in all_allergens:
            allergens[allergen] = all_ingredients.copy()

        found_ingredients = {}

        while len(found_ingredients) != len(all_ingredients):
            for allergen in allergens:
                if len(allergens[allergen]) == 1:
                    found_ingredients[allergen] = allergens[allergen][0]
                    self.remove_ingredients(allergen, allergens[allergen][0])

            for food_a in self.foods:
                if len(food_a.ingredients) == 1 and len(food_a.allergens) == 1:
                    found_ingredients[food_a.allergens[0]] = food_a.ingredients[0]

                    for allergen in all_allergens:
                        if food_a.ingredients[0] in allergen:
                            allergen.remove(food_a.ingredients)

                    self.remove_ingredients(food_a.allergens[0], food_a.ingredients[0])
                    continue

                for food_b in self.foods:
                    if food_a == food_b:
                        continue

                    union_allergens = [value for value in food_a.allergens if value in food_b.allergens]
                    union_ingredients = [value for value in food_a.ingredients if value in food_b.ingredients]

                    if len(union_allergens) == 1 and len(union_ingredients) == 1:
                        for allergen in all_allergens:
                            if union_ingredients[0] in allergen:
                                allergen.remove(union_ingredients)

                        found_ingredients[union_allergens[0]] = union_ingredients[0]
                        self.remove_ingredients(union_allergens[0], union_ingredients[0])

        return sum([len(x.allergens) for x in self.foods])


class Day21PartB(Day21, FileReaderSolution):
    def solve(self, input_data: str) -> int:
        self.parse_input(input_data)

        return 0