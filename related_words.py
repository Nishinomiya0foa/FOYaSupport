import Levenshtein


def get_equal_rate(str1, str2):
    return Levenshtein.ratio(str1, str2)


def get_the_most_similar(str1, iter_, more_similar=True, need_similar=False):
    similar = 0
    final_index = 0
    for index, r in enumerate(iter_):
        tmp = get_equal_rate(str1, r)
        if (more_similar and tmp > similar) or (not more_similar and tmp < similar):
            similar = tmp
            final_index = index
    res = [iter_[final_index], final_index]
    if need_similar:
        res.append(similar)
    return res


if __name__ == '__main__':
    ...