import Levenshtein


def get_equal_rate(str1, str2):
   return Levenshtein.ratio(str1, str2)