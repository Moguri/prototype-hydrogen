from direct.showbase.DirectObject import DirectObject
import direct.gui.DirectGui as dgui


class GameUI:
    def __init__(self):
        self.root = dgui.DirectFrame(
           frameColor=(0, 0, 0, 0),
           frameSize=(-1, 1, -1, 1),
           pos=(0, 0, 0)
        )

    def cleanup(self):
        self.root.destroy()


class GameState(DirectObject):
    def __init__(self, ui=None):
        self.ui = ui() if ui is not None else None

    def cleanup(self):
        self.ignoreAll()
        if self.ui:
            self.ui.cleanup()

    def run(self, dt):
        pass



class CombatUI(GameUI):
    pass


class CombatState(GameState):
    def __init__(self):
        super().__init__(CombatUI)

    def run(self, dt):
        pass

