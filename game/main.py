#!/usr/bin/env python3
import os
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))


from direct.showbase.ShowBase import ShowBase
import panda3d.core as p3d
import blenderpanda
from bamboo.inputmapper import InputMapper

import gamestates


p3d.load_prc_file_data(
    '',
    'model-path {}\n'.format('assets') + \
    'textures-power-2 none\n'
)


# Load config files
p3d.load_prc_file('config/game.prc')
if os.path.exists('config/user.prc'):
    print("Loading user.prc")
    p3d.load_prc_file('config/user.prc')
else:
    print("Did not find a user config")


class GameApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        blenderpanda.init(self)

        base.disableMouse()

        self.accept('quit', sys.exit)

        self.inputmapper = InputMapper('config/input.conf')

        self.current_state = None
        self.change_state(gamestates.CombatState)

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
