class Words(object):
    with open("words.txt") as words_file:
        words = list(map(lambda x: x.strip(), words_file))
        words_file.close()
    letter_frequencies = dict()
    for i in words:
        for j in i.lower():
            if j in letter_frequencies.keys():
                letter_frequencies[j] += 1.0
            else:
                letter_frequencies[j] = 1.0
    alphabet = list(letter_frequencies.keys())

    @staticmethod
    def get_frequency(word):
        out = dict()
        for i in word:
            if i in out:
                out[i] += 1
            else:
                out[i] = 1
        return out