import collections


class Deck:
    def __init__(self, card_master_list):
        self.__card_master_list = card_master_list

    @staticmethod
    def create(selected, card_master_list):
        deck_card_list = []
        for i in range(len(card_master_list)):
            if selected[i]:
                deck_card_list.append(card_master_list[i])
        return Deck(deck_card_list)

    def extend_card_master_list(self, card_master_list):
        self.__card_master_list.extend(card_master_list)

    def get_card_master_list(self):
        return self.__card_master_list

    def get_creature_mana_histogram_dictionary(self):
        ret = {}
        for card in self.__card_master_list:
            if 'Creature' not in card.basic_params.types:
                continue
            cmc = card.basic_params.cmc
            if cmc not in ret:
                ret[cmc] = 0
            ret[cmc] += 1
        return ret

    def get_noncreature_mana_histogram_dictionary(self):
        ret = {}
        for card in self.__card_master_list:
            if 'Creature' in card.basic_params.types:
                continue
            cmc = card.basic_params.cmc
            if cmc not in ret:
                ret[cmc] = 0
            ret[cmc] += 1
        return ret

    def get_color_set(self):
        ret = set()
        for card in self.__card_master_list:
            ret = ret.union(set(card.basic_params.colors))
        return ret

    def get_color_histogram(self):
        ret = {}
        for card in self.__card_master_list:
            for color in card.basic_params.colors:
                if color not in ret:
                    ret[color] = 0
                ret[color] += 1
        return ret

    def get_total_card_score(self):
        ret = 0
        for card in self.__card_master_list:
            ret += card.score
        return ret

    def print_for_mtg_arena(self):
        card_name_list = map(lambda card: card.to_mtg_arena_string(), self.__card_master_list)
        c = collections.Counter(card_name_list)
        for name, num in c.items():
            print('{0} {1}'.format(num, name))

    def write_file(self, file_name):
        sorted_deck_list = sorted(self.__card_master_list, key=lambda x: int(x.basic_params.number))
        tmp = {}
        for card in sorted_deck_list:
            if card.basic_params.name not in tmp:
                tmp[card.basic_params.name] = 0
            tmp[card.basic_params.name] += 1

        with open(file_name, 'w') as f:
            for key, value in tmp.items():
                f.write('{0} {1}\n'.format(value, key))
