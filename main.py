from models.mtg import *
from utils import *

cardScoreMasterRepository = CardScoreMasterRepository()
cardScoreMasterRepository.load_from_file('cardscores.txt')

cardMasterRepository = CardMasterRepository(cardScoreMasterRepository)
cardMasterRepository.load_from_file('database.dat')

card_master_list = []
with open('input.txt') as f:
    for line in f.read().splitlines():
        tmp = line.split(' ', 1)
        card_quantity = int(tmp[0])
        card_name = tmp[1]
        card_master = cardMasterRepository.get_by_card_name(card_name)
        # 土地は除外
        if 'Land' in card_master.basic_params.types:
            continue
        for i in range(card_quantity):
            card_master_list.append(cardMasterRepository.get_by_card_name(card_name))


def build():
    deck = DeckBuilder.build(card_master_list)

    BEST_LAND_QUANTITY = 17
    # 土地枚数はデッキの色に応じて均等に割り当てる
    # 例 デッキが赤・緑であれば 山9 森8
    land_list = []
    color_land_mapping = {'White': 'Plains', 'Blue': 'Island', 'Black': 'Swamp', 'Red': 'Mountain', 'Green': 'Forest'}
    deck_color_list = list(deck.get_color_histogram().keys())
    for color in deck_color_list:
        land = cardMasterRepository.get_by_card_name(color_land_mapping[color])
        for _ in range(int(BEST_LAND_QUANTITY / len(deck_color_list))):
            land_list.append(land)
    if len(deck.get_card_master_list()) + len(land_list) < 40:
        diff = 40 - len(deck.get_card_master_list()) - len(land_list)
        land = cardMasterRepository.get_by_card_name(color_land_mapping[deck_color_list[0]])
        for _ in range(diff):
            land_list.append(land)
    deck.extend_card_master_list(land_list)

    # deck.print_for_mtg_arena()
    deck.write_file('output.txt')


build()
