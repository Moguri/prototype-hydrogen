import random


ROLES = [
    'Single',
    'AoE',
    'Support',
]


TEMPLATES = {
    'swarmer': {
        'name': 'Swarmer',
        'health': 3,
        'attack': 3,
    },
    'heavy': {
        'name': 'Heavy',
        'health': 12,
        'attack': 12,
    },
    'skirmisher': {
        'name': 'Skirmisher',
        'health': 3,
        'attack': 12,
    },
    'tank': {
        'name': 'Tank',
        'health': 12,
        'attack': 3,
    },
}
class Character:
    def __init__(self):
        self.name = 'default'
        self.health = 3
        self.attack = 3
        self.target = None
        self.roles = []

    @classmethod
    def from_random(cls):
        result = Character()
        result.name = 'Random'

        stat_dist = [random.random() for i in range(2)]
        stat_sum = sum(stat_dist)
        stat_dist = [i / stat_sum for i in stat_dist]
        points = 24
        result.health = max(1, int(points * stat_dist[0]))
        result.attack = max(1, int(points * stat_dist[1]))

        num_roles = 2
        result.roles = random.sample(ROLES, num_roles)

        return result

    @classmethod
    def from_template(cls, template_name):
        template = TEMPLATES[template_name]

        result = Character()
        for key, value in template.items():
            setattr(result, key, value)
        result.roles.append('Monster')

        return result
