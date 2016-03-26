import random

from character import Character, TEMPLATES


TEMPLATE_COSTS = {
    'swarmer': 1,
    'heavy': 4,
    'skirmisher': 2,
    'tank': 2,
}


class Combatant:
    def __init__(self, name, character=None):
        self.role = 'Single'
        self._character = character if character else Character.from_random()

        self.hp_current = self.hp_max
        self.target = None

    @property
    def name(self):
        return self._character.name

    @property
    def attack(self):
        return self._character.attack

    @property
    def hp_max(self):
        return self._character.health

    @property
    def roles(self):
        return self._character.roles


class System:
    def act_single(self, actor, targets):
        if actor.hp_current > 0:
            damage = max(1, actor.attack // 2)
            targets[0].hp_current -= damage
            return '{} deals {} points of damage to {}\n'.format(actor.name, damage, targets[0].name)
        return ''

    def act_aoe(self, actor, targets):
        results = []
        if actor.hp_current > 0:
            damage = max(1, actor.attack // 6)
            for target in targets:
                target.hp_current -= damage
                results.append('{} deals {} points of damage to {}'.format(actor.name, damage, target.name))
        return '\n'.join(results)

    def act_support(self, actor, targets):
        results = []
        if actor.hp_current > 0:
            damage = max(1, actor.attack // 6)
            for target in targets:
                target.hp_current += damage
                results.append('{} heals {} points of damage to {}'.format(actor.name, damage, target.name))
        return '\n'.join(results)

    def __init__(self, player_list):
        self.player_list = [Combatant(c.name, c) for c in player_list]
        self.is_over = False

        self.enemy_list = []
        remaining_points = len(player_list) * 4
        options = list(TEMPLATES.keys())
        while remaining_points > 0:
            choice = random.choice(options)
            cost = TEMPLATE_COSTS[choice]
            if cost > remaining_points:
                continue
            remaining_points -= cost
            self.enemy_list.append(Character.from_template(choice))

        for i, enemy in enumerate(self.enemy_list):
            enemy.name = '({}) {}'.format(i, enemy.name)

        self.enemy_list = [Combatant(e.name, e) for e in self.enemy_list]

    def do_round(self, formation):
        enemy_role_list = ((enemy, 'Single') for enemy in self.enemy_list)

        actions = []
        remaining_enemies = [enemy for enemy in self.enemy_list if enemy.hp_current > 0]
        remaining_players = [p for p in self.player_list if p.hp_current > 0]
        for player, role in zip(self.player_list, formation):
            if player.hp_current <=0:
                continue
            targets = remaining_enemies
            if role == 'Single':
                if player.target:
                    targets = [player.target]
                else:
                    targets = [random.choice(remaining_enemies)]
            if role == 'Support':
                targets = self.player_list
            action = getattr(self, 'act_' + role.lower())
            actions.append((action, (player, targets)))
        for enemy in self.enemy_list:
            targets = [random.choice(remaining_players)]
            actions.append((self.act_single, (enemy, targets)))

        random.shuffle(actions)
        results = [act[0](*act[1]) for act in actions]

        remaining_enemies = [enemy for enemy in self.enemy_list if enemy.hp_current > 0]
        remaining_players = [p for p in self.player_list if p.hp_current > 0]

        self.is_over = len(remaining_players) == 0 or len(remaining_enemies) == 0

        return results
