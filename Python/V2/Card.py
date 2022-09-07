class Card:
    value = 0 # value of a specific card
    init_deck = [] # initial deck not shuffled
    current_deck = [] # current deck when we 
    symbols = [" club ", " diamond ", " heart ", " spade "]
    value_name = ['ace', '2', '3', '4', '5', '6', '7',    '8', '9', '10', 'jack', 'queen', 'king']
    club_deck = []
    diamond_deck = []
    heart_deck = []
    spade_deck = []
    for i in range(len(value_name)):
        club_deck.append(value_name[i] + symbols[0])
        diamond_deck.append(value_name[i] + symbols[1])
        heart_deck.append(value_name[i] + symbols[2])
        spade_deck.append(value_name[i] + symbols[3])

    init_deck = club_deck + diamond_deck + heart_deck + spade_deck