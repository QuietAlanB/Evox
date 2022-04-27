class GameManager:
        def __init__(self):
                self.creatures = []
                self.food = []

        def AddCreature(self, creature):
                self.creatures.append(creature)

        def RemoveCreature(self, creature):
                self.creatures.remove(creature)


        def AddFood(self, food):
                self.food.append(food)

        def RemoveFood(self, food):
                self.food.remove(food)


        def Update(self):
                for creature in self.creatures:
                        creature.Update()

                for food in self.food:
                        food.Update()

                        if food.eaten:
                                self.RemoveFood(food)


        def Draw(self):
                for food in self.food:
                        food.Draw()

                for creature in self.creatures:
                        creature.Draw()
