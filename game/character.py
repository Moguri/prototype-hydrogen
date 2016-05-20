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
        'position': 'BACK',
    },
    'heavy': {
        'name': 'Heavy',
        'health': 12,
        'attack': 12,
        'position': 'FRONT',
    },
    'skirmisher': {
        'name': 'Skirmisher',
        'health': 3,
        'attack': 12,
        'position': 'BACK',
    },
    'tank': {
        'name': 'Tank',
        'health': 12,
        'attack': 3,
        'position': 'FRONT',
    },
}
class Character:
    _serialize_fields = [
        'name',
        'health',
        'attack',
        'roles',
        'position'
    ]

    def __init__(self):
        self.name = 'default'
        self.health = 3
        self.attack = 3
        self.roles = []
        self.position = 'FRONT'

    def serialize(self):
        d = {field: getattr(self, field) for field in self._serialize_fields}

        return d

    def deserialize(self, d):
        for key, value in d.items():
            if key in self._serialize_fields:
                setattr(self, key, value)
            else:
                print("Warning: Unknown field to deserialize into Character: {}".format(key))


    @classmethod
    def from_random(cls):
        result = cls()
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

        result = cls()
        for key, value in template.items():
            setattr(result, key, value)
        result.roles.append('Monster')

        return result

    @classmethod
    def from_dictionary(cls, d):
        result = cls()
        result.deserialize(d)

        return result
