from collections import OrderedDict

from direct.showbase.DirectObject import DirectObject
import direct.gui.DirectGui as dgui
import panda3d.core as p3d


class GameUI:
    _roots = [
        ('root', 'aspect2d'),
        ('root_full', 'render2d'),
        ('root_left', 'a2dLeftCenter'),
        ('root_right', 'a2dRightCenter'),
    ]

    def __init__(self):
        for idx,root in enumerate(self._roots):
            setattr(self, root[0], dgui.DirectFrame(
                parent=getattr(base, root[1]),
                #frameColor=(0.2 * (idx+1), 0, 0, 0.5),
                frameColor=(0, 0, 0, 0),
                frameSize=(-1, 1, -1, 1),
                pos=(0, 0, 0)
            ))

    def cleanup(self):
        for root in self._roots:
            getattr(self, root[0]).destroy()


class GameState(DirectObject):
    def __init__(self, ui=None):
        self.ui = ui() if ui is not None else None
        self.root_node = p3d.NodePath('State Root')
        self.root_node.reparent_to(base.render)

    def cleanup(self):
        self.ignoreAll()
        if self.ui:
            self.ui.cleanup()
            self.ui = None
        self.root_node.remove_node()
        self.root_node = None

    def run(self, dt):
        pass



class CombatUI(GameUI):
    def __init__(self):
        super().__init__()

        self._pcs = OrderedDict()
        self._ecs = OrderedDict()

    def _create_pc_frame(self, n):
        frame = dgui.DirectFrame(
            parent=self.root_right,
            frameColor=(0.8, 0.8, 0.8, 0.5),
            frameSize=(-0.4, 0.4, -0.075, 0.075),
            pos=(-0.45 - 0.05 * n, 0, -0.55 - 0.175 * n)
        )

        frame.label = dgui.DirectLabel(
            parent=frame,
            text='',
            text_scale=(0.04, 0.04),
            text_align=p3d.TextNode.ALeft,
            frameColor=(0, 0, 0, 0),
            pos=(-0.375, 0, 0.04)
        )

        frame.hpbar = dgui.DirectWaitBar(
            parent=frame,
            value=100,
            text='0/0',
            text_scale=(0.025, 0.025),
            text_pos=(0, -0.01),
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 0.8),
            frameColor=(0, 0, 0, 1),
            frameSize=(-0.35, 0.35, -0.015, 0.015),
        )

        frame.rolelabel = dgui.DirectLabel(
            parent=frame,
            text='',
            text_scale=(0.03, 0.03),
            text_align=p3d.TextNode.ALeft,
            pos=(-0.3, 0, -0.05)
        )

        frame.attacklabel = dgui.DirectLabel(
            parent=frame,
            text='',
            text_scale=(0.03, 0.03),
            text_align=p3d.TextNode.ALeft,
            pos=(0, 0, -0.05),
        )

        return frame

    def _create_ec_frame(self, n, empty=False):
        frame_per_column = 12
        col = n // frame_per_column
        row = n % frame_per_column
        frame = dgui.DirectFrame(
            parent=self.root_left,
            frameColor=(0.8, 0.8, 0.8, 0.5),
            frameSize=(-0.2, 0.2, -0.08, 0.08),
            pos=(0.215 + 0.405 * col, 0, -1.075 + 0.167 * frame_per_column - 0.167 * row)
        )

        if not empty:
            frame.label = dgui.DirectLabel(
                parent=frame,
                text='',
                text_scale=(0.035, 0.035),
                text_align=p3d.TextNode.ALeft,
                frameColor=(0, 0, 0, 0),
                pos=(-0.175, 0, 0.025)
            )

            frame.hpbar = dgui.DirectWaitBar(
                parent=frame,
                value=100,
                text='0/0',
                text_scale=(0.025, 0.025),
                text_pos=(0, -0.006),
                text_fg=(1, 1, 1, 1),
                text_shadow=(0, 0, 0, 0.8),
                frameColor=(0, 0, 0, 1),
                frameSize=(-0.15, 0.15, -0.01, 0.01),
            )

            frame.rolelabel = dgui.DirectLabel(
                parent=frame,
                text='',
                text_scale=(0.025, 0.025),
                text_align=p3d.TextNode.ALeft,
                pos=(-0.15, 0, -0.05)
            )

            frame.attacklabel = dgui.DirectLabel(
                parent=frame,
                text='',
                text_scale=(0.025, 0.025),
                text_align=p3d.TextNode.ALeft,
                pos=(0.05, 0, -0.05),
            )

        return frame

    def setup_combatants(self, player_combatants, enemy_combatants):
        for combatant in player_combatants:
            self._pcs[combatant] = self._create_pc_frame(len(self._pcs))

        for combatant in enemy_combatants:
            self._ecs[combatant] = self._create_ec_frame(len(self._ecs))

        for i in range(len(self._ecs), 12):
            self._create_ec_frame(i, empty=True)

    def update_combatants(self, player_combatants, enemy_combatants):
        for combatant in player_combatants:
            ui = self._pcs[combatant]
            ui.label['text'] = combatant.name
            ui.hpbar['value'] = int(combatant.hp_current)
            ui.hpbar['text'] = '{}/{}'.format(int(combatant.hp_current), combatant.hp_max)
            ui.rolelabel['text'] = 'ROLE: {}'.format(combatant.role)
            ui.attacklabel['text'] = 'ATK: {}'.format(combatant.attack)

        for combatant in enemy_combatants:
            ui = self._ecs[combatant]
            ui.label['text'] = combatant.name
            ui.hpbar['value'] = int(combatant.hp_current)
            ui.hpbar['text'] = '{}/{}'.format(int(combatant.hp_current), combatant.hp_max)
            ui.rolelabel['text'] = 'ROLE: {}'.format(combatant.role)
            ui.attacklabel['text'] = 'ATK: {}'.format(combatant.attack)


class Combatant:
    def __init__(self, name):
        self.name = name
        self.role = 'Single'
        self.attack = 10
        self.hp_max = 100
        self.hp_current = 100


class CombatState(GameState):
    def __init__(self):
        super().__init__(CombatUI)

        self.player_combatants = [
            Combatant("Mech One"),
            Combatant("Mech Two"),
            Combatant("Mech Three"),
        ]

        self.enemy_combatants = [Combatant('Enemy {}'.format(i + 1)) for i in range(12)]

        self.ui.setup_combatants(self.player_combatants, self.enemy_combatants)

    def run(self, dt):
        for pc in self.player_combatants:
            pc.hp_current -= 5 * dt
            if pc.hp_current < 0:
                pc.hp_current = 0
        self.ui.update_combatants(self.player_combatants, self.enemy_combatants)

