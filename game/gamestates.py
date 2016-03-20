from direct.showbase.DirectObject import DirectObject

class GameState(DirectObject):
    def cleanup(self):
        self.ignoreAll()

    def run(self, dt):
        pass


class CombatState(GameState):
    def __init__(self):
        super().__init__()

    def run(self, dt):
        pass

