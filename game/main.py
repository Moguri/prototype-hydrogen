import os
import sys

from direct.showbase.ShowBase import ShowBase
import panda3d.core as p3d
import blenderpanda

import gamestates

p3d.load_prc_file_data(
    '',
    'model-path {}\n'.format(os.path.join(os.path.dirname(__file__), 'assets')) + \
    'framebuffer-srgb true\n'
)

class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        blenderpanda.init(self)
        self.accept('escape', sys.exit)

        self.current_state = gamestates.CombatState()
        def run_state(task):
            if self.current_state:
                self.current_state.run(globalClock.get_dt())
            return task.cont
        self.taskMgr.add(run_state, 'Game State')

    def change_state(self, next_state):
        if self.current_state:
            self.current_state.cleanup()
            self.current_state = None

        self.current_state = next_state()


app = GameApp()
app.run()
