import pickle
import random
import argparse
import sys


def levenshtein(a, b):
    # http://hetland.org/coding/python/levenshtein.py
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n
    current = range(n+1)
    for i in range(1, m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1, n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
    return current[n]


def decompound(word, dictionary):
    bits = []
    while word:
        choices = [w for w in dictionary[word[0]] if word.startswith(w) and len(w) > 1]
        if not choices:
            break
        longest_choice = max(choices, key=len)
        bits.append(longest_choice)
        word = word[len(longest_choice):]
    if word:  # unmatched leftovers
        bits.append(word)
    return bits


def emreggen(decompounded, bad_words, threshold=0.4):
    for bit in decompounded:
        options = [(w, levenshtein(bit.lower(), w.lower()) / len(bit)) for w in bad_words]
        valid_options = [(w, dist) for (w, dist) in options if dist <= threshold and w.lower() != bit.lower()]
        if valid_options:
            yield random.choice(valid_options)[0]
        else:
            yield bit


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('words', nargs='+')
    args = ap.parse_args()

    with open('wordtrie.pickle', 'rb') as inf:
        dct = pickle.load(inf)

    with open('badwords.txt', 'rt') as inf:
        bad_words = set(l.strip() for l in inf.readlines())

    words = []
    for word in args.words:
        words.extend(word.split(None))

    for word in words:
        decompounded = decompound(word, dct)
        print(decompounded, file=sys.stderr)
        reggened = emreggen(decompounded, bad_words)
        print(''.join(reggened), end=' ')
    print()


if __name__ == '__main__':
    main()
