from __future__ import print_function
from __future__ import division
import string
import re


def _edit_dist_init(len1, len2):
    lev = []
    for i in range(len1):
        lev.append([0] * len2)  # initialize 2D array to zero
    for i in range(len1):
        lev[i][0] = i           # column 0: 0,1,2,3,4,...
    for j in range(len2):
        lev[0][j] = j           # row 0: 0,1,2,3,4,...
    return lev


def _edit_dist_step(lev, i, j, s1, s2, transpositions=False, sub_cost=1):
    c1 = s1[i - 1]
    c2 = s2[j - 1]

    # skipping a character in s1
    a = lev[i - 1][j] + 1
    # skipping a character in s2
    b = lev[i][j - 1] + 1
    # substitution
    c = lev[i - 1][j - 1] + (sub_cost if c1 != c2 else 0)

    # transposition
    d = c + 1  # never picked by default
    if transpositions and i > 1 and j > 1:
        if s1[i - 2] == c2 and s2[j - 2] == c1:
            d = lev[i - 2][j - 2] + 1

    # pick the cheapest
    lev[i][j] = min(a, b, c, d)


def edit_distance(s1, s2, transpositions=False, sub_cost=1):
    """
    Calculate the Levenshtein edit-distance between two strings.
    The edit distance is the number of characters that need to be
    substituted, inserted, or deleted, to transform s1 into s2.  For
    example, transforming "rain" to "shine" requires three steps,
    consisting of two substitutions and one insertion:
    "rain" -> "sain" -> "shin" -> "shine".  These operations could have
    been done in other orders, but at least three steps are needed.

    This also optionally allows transposition edits (e.g., "ab" -> "ba"),
    though this is disabled by default.

    :param s1, s2: The strings to be analysed
    :param transpositions: Whether to allow transposition edits
    :type s1: str
    :type s2: str
    :type transpositions: bool
    :rtype int
    """
    # set up a 2-D array
    len1 = len(s1)
    len2 = len(s2)
    lev = _edit_dist_init(len1 + 1, len2 + 1)

    # iterate over the array
    for i in range(len1):
        for j in range(len2):
            _edit_dist_step(lev, i + 1, j + 1, s1, s2, transpositions=transpositions, sub_cost=sub_cost)
    return lev[len1][len2]


def clean_addr(s):
    s = s.lower()
    s = s.translate(string.maketrans('', ''), string.punctuation)
    s = re.sub(r'\bstreet\b', r'st', s)
    s = re.sub(r'\broad\b', r'rd', s)
    s = re.sub(r'\bavenue\b', r'av', s)
    s = re.sub(r'\bdrive\b', r'dr', s)
    s = re.sub(r'\bboulevard\b', r'bd', s)
    s = re.sub(r'\bblvd\b', r'bd', s)
    s = re.sub(r'\bnorth\b', r'n', s)
    s = re.sub(r'\bsouth\b', r's', s)
    s = re.sub(r'\bwest\b', r'w', s)
    s = re.sub(r'\beast\b', r'e', s)
    s = re.sub(r' +', r' ', s)
    p = s.find('detroit mi')
    if p != -1:
        s = s[:p]
    p = s.find('detroitmi')
    if p != -1:
        s = s[:p]
    s = s.strip()
    return s


def is_same_addr(x, y):
    xt = x.split()
    yt = y.split()
    xs = set(xt)
    ys = set(yt)

    # if start with road number, it has to match
    flag_start_with_number = xt[0].isdigit() and yt[0].isdigit()
    flag_number_match = (xt[0] == yt[0])

    num_tokens_match = len(xs.intersection(ys))

    # this accounts for typos
    flag_edit_dist_ok = (edit_distance(x, y, sub_cost=2) < 7)

    if flag_start_with_number:
        if flag_number_match and num_tokens_match >= 1 and flag_edit_dist_ok:
            return True
    else:
        if num_tokens_match >= 1 and flag_edit_dist_ok:
            return True

    return False
