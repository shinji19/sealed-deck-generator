import pickle

from models.mtg import CardMaster


class CardMasterRepository:
    def __init__(self, card_score_master_repository):
        self.__card_score_master_repository = card_score_master_repository
        self.__card_dictionary = {}
        self.__card_list = []

    def load_from_file(self, file_path):
        card_list = []
        with open(file_path, 'rb') as f:
            card_list = pickle.load(f)

        self.__card_dictionary = {}
        self.__card_list = []
        for card in card_list:
            score = self.__card_score_master_repository.get_by_card_name(card.name)
            card_master = CardMaster(card, score)
            self.__card_list.append(card_master)
            self.__card_dictionary[card.name] = card_master

    def get_all(self):
        return self.__card_list

    def get_by_card_name(self, name):
        return self.__card_dictionary[name]

    def dump(self):
        print('----- card master repository -----')
        print('count:{0}'.format(len(self.__card_list)))
        for card in self.__card_list:
            print('{0} ({1}) {2}'.format(card.name, card.set, card.number))
        print('-----')
