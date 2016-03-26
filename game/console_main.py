import itertools
import os
import shutil

from character import Character
import combat


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def display_player(mechs):
    con_width = shutil.get_terminal_size().columns
    mechs_per_line = con_width // 20 - 1

    if len(mechs) > mechs_per_line:
        display_player(mechs[:mechs_per_line])
        display_player(mechs[mechs_per_line:])
    else:
        hor_sep = '-' * 19 + '+'
        hor_sep = '+' + '-' * 18 + '+' + hor_sep * (len(mechs))
        print(hor_sep)
        line = ''.join([mech.name + ' ' * (19-len(mech.name)) + '|' for mech in mechs])
        line = '|Name              |' + line
        print(line)
        line = ''.join(['{: <19}|'.format(mech.health) for mech in mechs])
        line = '|Health            |' + line
        print(line)
        line = ''.join(['{: <19}|'.format(mech.attack) for mech in mechs])
        line = '|Attack            |' + line
        print(line)

        max_roles = max([len(mech.roles) for mech in mechs])
        for i in range(max_roles):
            roles = [mech.roles[i] if len(mech.roles) > i else '' for mech in mechs]
            line = ''.join([role + ' ' * (19-len(role)) + '|' for role in roles])
            if i == 0:
                line = '|Roles:            |' + line
            else:
                line = '|                  |' + line
            print(line)

        print(hor_sep)

def pick_target(combat_sys, player):
    target = None
    while target == None:
        clear()
        display_player(combat_sys.enemy_list)
        target_idx = input('Pick target for {}: '.format(player.name))
        try:
            target_idx = int(target_idx)
            target = combat_sys.enemy_list[target_idx]
        except:
            continue

    player.target = target


def main():
    names = ('Alpha', 'Beta', 'Gamma', 'Delta', 'Epsilon')
    mechs = [Character.from_random() for i in range(3)]
    for i, mech in enumerate(mechs):
        mech.name = names[i%len(names)]

    formations = []
    for i in mechs[0].roles:
        for j in mechs[1].roles:
            for k in mechs[2].roles:
                formations.append((i, j, k))

    combat_sys = combat.System(mechs)

    while not combat_sys.is_over:
        clear()
        display_player(combat_sys.enemy_list)
        display_player(mechs)

        for i, formation in enumerate(formations):
            print(i, ', '.join(formation))

        formation_idx = input('Choose a formation: ')
        try:
            formation_idx = int(formation_idx)
            formation = formations[formation_idx]
        except:
            continue

        for mech, role in zip(mechs, formation):
            if role == 'Single' and mech.health > 0:
                pick_target(combat_sys, mech)
                print(mech.target)

        clear()
        results = combat_sys.do_round(mechs, formation)
        for result in results:
            print(result)
        input('Press enter to continue')

    clear()
    display_player(combat_sys.enemy_list)
    display_player(mechs)


main()
