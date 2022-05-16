from random import choice

class Card:
    def __init__(self, card_index):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

        suit_index = card_index // 13
        value_index = card_index % 13

        self.value = values[value_index]

        self.image = f"card_images/{value_index:02d}_{suit_index:02d}"

def draw_card():
    global card_indexes
    
    if card_indexes == []:
        for x in range(52):
            card_indexes.append(x)

    card_index = choice(card_indexes) 
    new_card = Card(card_index)

    card_indexes.remove(card_index)

    return new_card

card_indexes = []
for x in range(52):
    card_indexes.append(x)
