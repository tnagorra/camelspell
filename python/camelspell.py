import vim
import re

cc_re = re.compile(r'[0-9A-Za-z]+(?:[A-Z][a-z0-9]+|(?<![A-Z])[A-Z]+)(?!\w)')
first_cap_re = re.compile('(.)([A-Z][a-z]+)')
all_cap_re = re.compile('([a-z0-9])([A-Z])')

# Use same data structure
all_bad_words = {}


def _convert(word):
    foo = first_cap_re.sub(r'\1_\2', word)
    bar = all_cap_re.sub(r'\1_\2', foo).lower()
    return bar.split('_')


def _spellcheck_word(word):
    op = vim.eval('spellbadword("{}")'.format(word))
    return op[0] != ''


def _find_cc_words(sentence):
    return cc_re.findall(sentence)


def _find_all_cc_words(sentences):
    cc_words = set()
    for sentence in sentences:
        words = _find_cc_words(sentence)
        if words is not None:
            cc_words |= set(words)
    return cc_words


def is_bad_word(cc_word):
    sub_words = _convert(cc_word)
    if sub_words:
        bad_sub_words = filter(_spellcheck_word, sub_words)
        return any(bad_sub_words)
    return False


def spell_check():
    global all_bad_words
    buffer_id = vim.current.buffer
    bad_words = all_bad_words.get(buffer_id, {})

    # Get lines from current buffer
    lines = vim.eval('getline(1,"$")')

    new_bad_words = {s for s in _find_all_cc_words(lines) if is_bad_word(s)}

    words_to_delete = bad_words.keys() - new_bad_words
    words_to_add = new_bad_words - bad_words.keys()

    # Remove from bad_words and delete match
    for word in words_to_delete:
        identifier = bad_words.pop(word)
        vim.eval('matchdelete({})'.format(identifier))

    # Add to bad_words and add match
    for word in words_to_add:
        bad_words[word] = vim.eval(
            'matchadd("CamelCaseError", "{}")'.format(word)
        )

    # set bad_words to all_bad_words
    all_bad_words[buffer_id] = bad_words


def display_spell_mistakes():
    buffer_id = vim.current.buffer
    bad_words = all_bad_words.get(buffer_id, {})

    for word in sorted(bad_words.keys()):
        print(word)
