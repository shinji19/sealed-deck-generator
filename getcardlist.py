from mtgsdk import Card
import pickle

DATABASE_FILE_NAME = 'database.dat'


def fetch():
    print('Start request...')
    card_all = Card.where(set='M21').all()
    print('Success request!')
    cards = []
    for c in card_all:
        # 番外カードは除外する
        if int(c.number) < 275:
            cards.append(c)
    cards.sort(key=lambda x: int(x.number))
    return cards


def save(card_list):
    with open(DATABASE_FILE_NAME, 'wb') as f:
        pickle.dump(card_list, f)


def load():
    ret = []
    with open(DATABASE_FILE_NAME, 'rb') as f:
        ret = pickle.load(f)
    return ret


def main():
    card_list = fetch()
    save(card_list)
    card_list = load()
    for card in card_list:
        print('{0} ({1}) {2}'.format(card.name, card.set, card.number))


if __name__ == '__main__':
    main()
