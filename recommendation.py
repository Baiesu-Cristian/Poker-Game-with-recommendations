simple = [['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
          ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
          ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H'],
          ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
          ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
          ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
          ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
          ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H']]

aces = [['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
        ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
        ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
        ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
        ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
        ['S', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'],
        ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
        ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']]

split = [['s', 's', 's', 's', 's', 's', 'H', 'H', 'H', 'H'],
         ['s', 's', 's', 's', 's', 's', 'H', 'H', 'H', 'H'],
         ['H', 'H', 'H', 's', 's', 'H', 'H', 'H', 'H', 'H'],
         ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
         ['s', 's', 's', 's', 's', 'H', 'H', 'H', 'H', 'H'],
         ['s', 's', 's', 's', 's', 's', 'H', 'H', 'H', 'H'],
         ['s', 's', 's', 's', 's', 's', 's', 's', 's', 's'],
         ['s', 's', 's', 's', 's', 'S', 's', 's', 'S', 'S']]

full = {'H':"hit", 'S':"stand", 'D':"double", 's':"split"}

def simple_rec(player, dealer):
    if player >= 17:
        return "stand"
    elif player <= 8:
        return "hit"
    else:
        return full[simple[player-9][dealer-2]]

def aces_rec(player, dealer):
    if player >= 8:
        return "stand"
    else:
        return full[aces[player-2][dealer-2]]

def split_rec(player, dealer):
    if player == 11:
        return "split"
    elif player == 10:
        return "stand"
    else:
        return full[split[player-2][dealer-2]]

