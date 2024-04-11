import random


class Variants:
    def __init__(self):
        self.variants = []
        self.fill_variants()

    def fill_variants(self):
        with open('engwords.txt') as f:
            for w in f:
                self.variants.append(w.strip().capitalize())

    def choose_variants(self):
        chosen_words = []
        for i in range(3):
            random_w = random.choice(self.variants)
            chosen_words.append(random_w)
            self.variants.remove(random_w)
        return chosen_words


variants = Variants()

if __name__ == '__main__':
    pass
