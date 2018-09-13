import vim
import re

camelcase_re = re.compile(r'[0-9A-Za-z]+(?:[A-Z][a-z0-9]+|(?<![A-Z])[A-Z]+)(?!\w)')
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

bad_camelcase_words = {}
match_keys = {}


def memoize(func):
    cache = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func


@memoize
def convert(word):
    foo = first_cap_re.sub(r'\1_\2', word)
    bar = all_cap_re.sub(r'\1_\2', foo).lower()
    return bar.split('_')


@memoize
def spellcheck_word(word):
    op = vim.eval('spellbadword("{}")'.format(word))
    return op[0] != ''


@memoize
def find_camelcase_words(sentence):
    return camelcase_re.findall(sentence)


def spell_check():
    global bad_camelcase_words
    buffer_id = vim.current.buffer

    # must be dict
    current_bad_camelcase_words = bad_camelcase_words.get(buffer_id, set())
    # must be emptyset if not
    current_match_keys = match_keys.get(buffer_id, {})

    lines = vim.eval('getline(1,"$")')
    camelcase_words = set()
    for line in lines:
        words = find_camelcase_words(line)
        if words is not None:
            camelcase_words |= set(words)

    new_bad_camelcase_words = set()
    for camelcase_word in camelcase_words:
        sub_words = convert(camelcase_word)
        if sub_words:
            bad_sub_words = filter(spellcheck_word, sub_words)
            if any(bad_sub_words):
                new_bad_camelcase_words.add(camelcase_word)

    obsolete_words = current_bad_camelcase_words - new_bad_camelcase_words
    hot_words = new_bad_camelcase_words - current_bad_camelcase_words

    if hot_words:
        for word in hot_words:
            current_match_keys[word] = vim.eval(
                'matchadd("CamelCaseError", "{}")'.format(word)
            )
    match_keys[buffer_id] = current_match_keys

    if obsolete_words:
        for word in obsolete_words:
            id = current_match_keys.pop(word)
            vim.eval('matchdelete({})'.format(id))

    bad_camelcase_words[buffer_id] = new_bad_camelcase_words


def display_spell_mistakes():
    buffer_id = vim.current.buffer
    current_bad_camelcase_words = bad_camelcase_words.get(buffer_id, set())
    current_match_keys = match_keys.get(buffer_id, {})

    for word in sorted(current_bad_camelcase_words):
        print(word, current_match_keys.get(word))
