import random
from deap import creator, base, tools, algorithms
from models.mtg import Deck


class DeckBuilder:
    # 理想的なマナカーブを表す
    BEST_CREATURE_MANA_HISTOGRAM = {2: 4, 3: 5, 4: 4, 5: 2, 6: 1}
    # 理想的なクリーチャー以外のスペル枚数を表す
    BEST_NONCREATURE_QUANTITY = 7

    # 評価の重み
    DECK_CARD_QUANTITY_WEIGHT = 100  # デッキ枚数の評価の重み
    CREATURE_MANA_CURVE_WEIGHT = 50  # クリーチャーのマナカーブの評価の重み
    NONCREATURE_QUANTITY_WEIGHT = 100  # クリーチャー以外のマナカーブの評価の重み
    CARD_SCORE_WEIGHT = 100  # カードのスコアの評価の重み
    COLOR_WEIGHT = 200  # デッキの色数の評価の重み

    # 個体評価関数
    @staticmethod
    def eval_one_max(individual, card_master_list):
        score = 0
        deck = Deck.create(individual, card_master_list)

        # デッキ枚数ペナルティ
        best_card_quantity = sum(DeckBuilder.BEST_CREATURE_MANA_HISTOGRAM.values()) + DeckBuilder.BEST_NONCREATURE_QUANTITY
        score -= abs(best_card_quantity - len(deck.get_card_master_list())) / len(card_master_list) * DeckBuilder.DECK_CARD_QUANTITY_WEIGHT

        # クリーチャーのマナカーブに剃っていないペナルティ
        creature_mana_histogram_dictionary = deck.get_creature_mana_histogram_dictionary()
        creature_mana_curve_diff = 0
        for mana, value in creature_mana_histogram_dictionary.items():
            if mana in DeckBuilder.BEST_CREATURE_MANA_HISTOGRAM:
                creature_mana_curve_diff += abs(value - DeckBuilder.BEST_CREATURE_MANA_HISTOGRAM[mana])
            else:
                creature_mana_curve_diff += value
        creature_max_diff = len(card_master_list) + sum(DeckBuilder.BEST_CREATURE_MANA_HISTOGRAM.values())
        score -= creature_mana_curve_diff / float(creature_max_diff) * DeckBuilder.CREATURE_MANA_CURVE_WEIGHT

        # クリーチャー以外の枚数ペナルティ
        noncreature_mana_histogram_dictionary = deck.get_noncreature_mana_histogram_dictionary()
        noncreature_quantity = sum(noncreature_mana_histogram_dictionary.values())
        noncreature_max_diff = DeckBuilder.BEST_NONCREATURE_QUANTITY + len(card_master_list)
        score -= abs(DeckBuilder.BEST_NONCREATURE_QUANTITY - noncreature_quantity) / float(
            noncreature_max_diff) * DeckBuilder.NONCREATURE_QUANTITY_WEIGHT

        # カード評価のスコア
        max_card_score = sum(map(lambda x: x.score, card_master_list))
        score += deck.get_total_card_score() / float(max_card_score) * DeckBuilder.CARD_SCORE_WEIGHT

        # 色のスコア
        color_histogram = deck.get_color_histogram()
        sorted_color_quantity = sorted(color_histogram.values(), reverse=True)
        cnt = 0
        non_main_color_card_quantity = 0
        for color_quantity in sorted_color_quantity:
            # カード枚数を多い順にソートして一番多かったものと二番に多かったものをメインカラーとして
            # それ以外の色をデッキに組み込んでいる場合はペナルティを与える
            if cnt > 1:
                non_main_color_card_quantity += color_quantity
            cnt += 1
        max_non_main_color_card_quantity = len(card_master_list)
        score -= non_main_color_card_quantity / float(max_non_main_color_card_quantity) * DeckBuilder.COLOR_WEIGHT

        return score,

    # GAに関するパラメータ
    INDPB = 0.05  # 遺伝子突然変異率
    TOURNSIZE = 3  # トーナメント選択のサイズ
    N = 300  # 世代内個体数
    CXPB = 0.5  # 交叉率
    MUTPB = 0.1  # 個体突然変異率
    NGEN = 100  # ループ回数

    @staticmethod
    def build(card_master_list):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(card_master_list))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", DeckBuilder.eval_one_max, card_master_list=card_master_list)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=DeckBuilder.INDPB)
        toolbox.register("select", tools.selTournament, tournsize=DeckBuilder.TOURNSIZE)

        population = toolbox.population(n=DeckBuilder.N)

        for gen in range(DeckBuilder.NGEN):
            offspring = algorithms.varAnd(population, toolbox, cxpb=DeckBuilder.CXPB, mutpb=DeckBuilder.MUTPB)
            fits = toolbox.map(toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
            population = toolbox.select(offspring, k=len(population))
            top = tools.selBest(population, k=1)
            print('deck score: {0}'.format(DeckBuilder.eval_one_max(top[0], card_master_list)))
        top10 = tools.selBest(population, k=10)

        deck = Deck.create(top10[0], card_master_list)
        return deck
