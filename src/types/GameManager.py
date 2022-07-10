class GameManager:
        def __init__(self):
                self.creatures = []

        def DrawUpdate(self):
                for creature in self.creatures:
                        creature.DrawUpdate()

        def GameUpdate(self):
                for creature in self.creatures:
                        creature.GameUpdate()