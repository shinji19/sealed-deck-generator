

class CardScoreMasterRepository:
    def __init__(self):
        self.__score_dictionary = {}

    def load_from_file(self, file_path):
        ret = {}
        with open(file_path) as f:
            for line in f.read().splitlines():
                tmp = line.split(' ', 1)
                score = float(tmp[0])
                card_name = tmp[1]
                ret[card_name] = score
        self.__score_dictionary = ret

    def get_by_card_name(self, name):
        return self.__score_dictionary[name]

    def dump(self):
        print('----- card score master repository -----')
        print('count:{0}'.format(len(self.__score_dictionary.keys())))
        for card_name, score in self.__score_dictionary.items():
            print('{0} {1}'.format(score, card_name))
        print('-----')
