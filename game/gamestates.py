from collections import OrderedDict
import json
import random
import sys

from direct.showbase.DirectObject import DirectObject
import direct.gui.DirectGui as dgui
import panda3d.core as p3d


class SaveData:
    def __init__(self):
        names = ('Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon')
        self.mechs = [Character.from_random() for i in range(3)]
        for i, character in enumerate(self.mechs):
            character.name = names[i%len(names)]

    def serialize(self):
        d = {
            'mechs': [mech.serialize() for mech in self.mechs],
        }

        return d

    def deserialize(self, d):
        for key, value in d.items():
            if key == 'mechs':
                self.mechs = [Character.from_dictionary(i) for i in value]
            else:
                print("Warning: Unknown field to deserialize into SaveData: {}".format(key))

    def write(self, fpath):
        with open(fpath, 'w') as f:
            json.dump(self.serialize(), f)

    @classmethod
    def from_file(cls, fpath):
        sd = cls()

        with open(fpath) as f:
            sd.deserialize(json.load(f))

        return sd


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


class TitleUI(GameUI):
    def __init__(self):
        super().__init__()
        self._selection_items = []

        dgui.DirectFrame(
            parent=self.root_full,
            image='landscape.png',
            frameSize=(-1.0, 1.0, -1.0, 1.0)
        )

        dgui.DirectLabel(
            parent=self.root,
            text='Prototype Hydrogen',
            text_scale=(0.15, 0.15),
            frameColor=(0, 0, 0, 0),
            pos=(0.0, 0.0, 0.8)
        )

    def setup_selections(self, selections, select_cb):
        for i in self._selection_items:
            i.destroy()
        self._selection_items = []

        for idx, selection in enumerate(selections):
            btn = dgui.DirectButton(
                parent=self.root,
                command=select_cb,
                extraArgs=[selection],
                text=selection,
                text_scale=(0.05, 0.05),
                text_pos=(0, -0.02),
                relief=dgui.DGG.FLAT,
                frameColor=(0.3, 0.3, 0.3, 0.5),
                frameSize=(-0.25, 0.25, -0.04, 0.04),
                pos=(0, 0, 0.4 - 0.15 * idx)
            )
            self._selection_items.append(btn)


class TitleState(GameState):
    def __init__(self):
        super().__init__(TitleUI)

        options = [
            "New Game",
            "Load Game",
            "Options",
            "Exit",
        ]

        self.ui.setup_selections(options, self.do_selection)

    def do_selection(self, option):
        if option == "New Game":
            base.change_state(MainState)
        elif option == "Load Game":
            print("Loading not implemented, starting new game")
            base.change_state(MainState)
        elif option == "Options":
            print("Options not implemented")
        elif option == "Exit":
            sys.exit()


class MainUI(GameUI):
    def __init__(self):
        super().__init__()
        self._selection_items = []

        dgui.DirectFrame(
            parent=self.root_full,
            frameColor=(0.8, 0.8, 0.8, 0.8),
            frameSize=(-1.0, 1.0, -1.0, 1.0)
        )

    def setup_selections(self, selections, select_cb):
        for i in self._selection_items:
            i.destroy()
        self._selection_items = []

        for idx, selection in enumerate(selections):
            btn = dgui.DirectButton(
                parent=self.root_left,
                command=select_cb,
                extraArgs=[selection],
                text=selection,
                text_scale=(0.05, 0.05),
                text_pos=(0, -0.02),
                relief=dgui.DGG.FLAT,
                frameColor=(0.3, 0.3, 0.3, 0.5),
                frameSize=(-0.25, 0.25, -0.04, 0.04),
                pos=(0.2, 0, 0.3 - 0.15 * idx)
            )
            self._selection_items.append(btn)


class MainState(GameState):
    def __init__(self):
        super().__init__(MainUI)

        options = [
            "Start Combat",
            "Enter Shop",
            "Mech Status",
            "Save",
            "Load",
            "Options",
            "Exit",
        ]

        self.ui.setup_selections(options, self.do_selection)

    def do_selection(self, option):
        if option == "Start Combat":
            base.change_state(CombatState)
        elif option == "Exit":
            sys.exit()
        else:
            print("Not implemented: {}".format(option))


class ShopUI(GameUI):
    def __init__(self):
        super().__init__()


class ShopState(GameState):
    def __init__(self):
        super().__init__(ShopUI)


class CombatUI(GameUI):
    def __init__(self):
        super().__init__()

        self._pcs = OrderedDict()
        self._ecs = OrderedDict()

        self._selection_frame = None
        self._selection_items = []

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

        frame.attacklabel = dgui.DirectLabel(
            parent=frame,
            text='',
            text_scale=(0.03, 0.03),
            text_align=p3d.TextNode.ALeft,
            pos=(-0.375, 0, -0.05),
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


            frame.attacklabel = dgui.DirectLabel(
                parent=frame,
                text='',
                text_scale=(0.025, 0.025),
                text_align=p3d.TextNode.ALeft,
                pos=(-0.175, 0, -0.05),
            )

        return frame

    def setup_combatants(self, player_combatants, enemy_combatants):
        for combatant in player_combatants:
            self._pcs[combatant] = self._create_pc_frame(len(self._pcs))

        for combatant in enemy_combatants:
            self._ecs[combatant] = self._create_ec_frame(len(self._ecs))

        for i in range(len(self._ecs), 12):
            self._create_ec_frame(i, empty=True)

    def setup_selections(self, title, selections, select_cb):
        if self._selection_frame:
            self._selection_frame.destroy()
            self._selection_frame = None

            for i in self._selection_items:
                i.destroy()
            self._selection_items = []

        num_items = len(selections)
        frame_size = num_items / 10.0 + 0.06

        self._selection_frame = dgui.DirectFrame(
            parent=self.root,
            frameColor=(0.8, 0.8, 0.8, 0.5),
            frameSize=(-0.25, 0.25, 0.0, frame_size),
            pos=(0, 0, -1.0)
        )

        dgui.DirectLabel(
            parent=self._selection_frame,
            text=title,
            text_scale=(0.05, 0.05),
            frameColor=(0, 0, 0, 0),
            pos=(0, 0, frame_size)
        )

        for idx, selection in enumerate(selections):
            btn = dgui.DirectButton(
                parent=self.root,
                command=select_cb,
                extraArgs=[idx],
                text=selection,
                text_scale=(0.03, 0.03),
                text_pos=(0, -0.01),
                relief=dgui.DGG.FLAT,
                frameColor=(0.3, 0.3, 0.3, 0.5),
                frameSize=(-0.25, 0.25, -0.04, 0.04),
                pos=(0, 0, (0.1 * num_items - 1.02) - 0.1 * idx)
            )
            self._selection_items.append(btn)

    def update_combatants(self, player_combatants, enemy_combatants):
        for combatant in player_combatants:
            ui = self._pcs[combatant]
            ui.label['text'] = combatant.name
            ui.hpbar['value'] = int(combatant.hp_current / combatant.hp_max * 100)
            ui.hpbar['text'] = '{}/{}'.format(int(combatant.hp_current), combatant.hp_max)
            ui.attacklabel['text'] = 'ATK: {}'.format(combatant.attack)

        for combatant in enemy_combatants:
            ui = self._ecs[combatant]
            ui.label['text'] = combatant.name
            ui.hpbar['value'] = int(combatant.hp_current / combatant.hp_max * 100)
            ui.hpbar['text'] = '{}/{}'.format(int(combatant.hp_current), combatant.hp_max)
            ui.attacklabel['text'] = 'ATK: {}'.format(combatant.attack)


from character import Character
import combat


class CombatState(GameState):
    def __init__(self):
        super().__init__(CombatUI)

        scene = loader.loadModel('arena.bam')
        camera = scene.find('Camera')
        base.cam.set_pos(camera.get_pos())
        base.cam.look_at(p3d.LVector3(0, 0, 0))
        scene.reparent_to(self.root_node)

        self.selected_formation = None
        self.selected_targets = False

        if base.save_data is None:
            print("Warning: No save data in combat state, using random mechs")
            save_data = SaveData()
        else:
            save_data = base.save_data

        self.player_characters = save_data.mechs

        self.formations = []
        self.formation_idx = -1
        for i in self.player_characters[0].roles:
            for j in self.player_characters[1].roles:
                for k in self.player_characters[2].roles:
                    self.formations.append((i, j, k))
        self.formation_items = [
            '({}) {} | {} | {}'.format(idx + 1, *items) for idx, items in enumerate(self.formations)
        ]

        self.combat_sys = combat.System(self.player_characters)
        self.ui.setup_combatants(self.combat_sys.player_list, self.combat_sys.enemy_list)

        # Place enemy models
        enemy_models = {
            'heavy' : loader.loadModel('heavy.bam'),
            'skirmisher' : loader.loadModel('skirmisher.bam'),
            'swarmer' : loader.loadModel('swarmer.bam'),
            'tank' : loader.loadModel('tank.bam'),
        }
        enemy_node = scene.attachNewNode('enemies')
        for i, enemy in enumerate(self.combat_sys.enemy_list):
            x = i % 2
            y = i // 2
            key = enemy.name.split(' ')[1].lower()
            model = enemy_node.attachNewNode(enemy.name)
            model.set_pos(x * 4 - 6, y * -4 + 5, 0)
            enemy_models[key].instanceTo(model)

        # Place player models
        player_node = scene.attachNewNode('players')
        player_model = loader.loadModel('player.bam')
        for i, player in enumerate(self.combat_sys.player_list):
            model = player_node.attachNewNode(player.name)
            model.set_pos(5, i * -4 + 4, 0)
            player_model.instanceTo(model)

        self.accept('selection1', self.select_item, [0])
        self.accept('selection2', self.select_item, [1])
        self.accept('selection3', self.select_item, [2])
        self.accept('selection4', self.select_item, [3])
        self.accept('selection5', self.select_item, [4])
        self.accept('selection6', self.select_item, [5])
        self.accept('selection7', self.select_item, [6])
        self.accept('selection8', self.select_item, [7])
        self.accept('selection9', self.select_item, [8])
        self.accept('selection0', self.select_item, [9])

    def select_item(self, idx):
        self.formation_idx = idx

    def run(self, dt):
        current_player = None
        for player in self.combat_sys.player_list:
            if player.role == 'Single' and player.target == None and player.hp_current > 0:
                current_player = player
                break
        else:
            self.selected_targets = True

        if self.combat_sys.is_over:
                print('Combat is over')
        elif self.formation_idx != -1 and self.selected_formation == None:
            self.selected_formation = self.formations[self.formation_idx]
            for player, role in zip(self.combat_sys.player_list, self.selected_formation):
                player.role = role
            self.formation_idx = -1
            self.selected_targets = False
        elif self.selected_formation:
            if self.formation_idx != -1 and not self.selected_targets:
                current_player.target = self.combat_sys.enemy_list[self.formation_idx]
                self.formation_idx = -1
            elif not self.selected_targets and self.formation_idx == -1:
                #print('Select target for {}'.format(current_player.name))
                self.ui.setup_selections(
                    'Select Target for {}'.format(current_player.name),
                    [i.name for i in self.combat_sys.enemy_list],
                    self.select_item
                )
            elif self.selected_targets:
                results = self.combat_sys.do_round(self.selected_formation)
                self.selected_formation = None
                for player in self.combat_sys.player_list:
                    player.target = None
                    np = self.root_node.find('**/players/' + player.name)
                    if player.hp_current > 0:
                        np.show()
                    else:
                        np.hide()
                for result in results:
                    print(result)
                for enemy in self.combat_sys.enemy_list:
                    np = self.root_node.find('**/enemies/'+enemy.name)
                    if enemy.hp_current > 0:
                        np.show()
                    else:
                        np.hide()
        else:
            self.ui.setup_selections('Select Formation', self.formation_items, self.select_item)

        self.ui.update_combatants(self.combat_sys.player_list, self.combat_sys.enemy_list)
