class CardMaster:
    def __init__(self, basic_params, score):
        self.basic_params = basic_params
        self.score = score

    def __str__(self):
        return "{0} {1}".format(self.basic_params.name, self.score)

    def to_mtg_arena_string(self):
        return '{0} ({1}) {2}'.format(self.basic_params.name, self.basic_params.set, self.basic_params.number)
