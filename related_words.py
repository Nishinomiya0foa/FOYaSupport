import Levenshtein


def get_equal_rate(str1, str2):
    return Levenshtein.ratio(str1, str2)


def get_the_most_similar(str1, iter_):
    similar = 0
    final_index = 0
    for index, r in enumerate(iter_):
        tmp = get_equal_rate(str1, r)
        if tmp > similar:
            similar = tmp
            final_index = index
    return iter_[final_index], final_index
