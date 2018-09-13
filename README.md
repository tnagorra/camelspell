# camelspell

Support spell checking of camelCase words.
It overrides vim's built in spellchecker for camelCase words.

## Installation

Before installation, please check your Vim supports python by running `:echo has('python3')`.
You can install camelspell like any other plugins.

### Vim Plug

Add the plugin in your ``.vimrc``

```
Plug 'tnagorra/camelspell'
```

Run the following commands:

```
:source %
:PlugInstall
```

## Usage

- Run ':CamelspellCheck' to check for camelCase spelling mistakes.
- Run ':CamelspellList' to list camelCase spelling mistakes.


## Options

```
" Time after which spell check will be run after text is changed
let g:camelspell_delay = 100

" Invoke spell check on file open
let g:camelspell_check_on_startup = 1

" Invoke spell check on text change
let g:camelspell_check_on_text_change = 1

" Invoke spell check on save
let g:camelspell_check_on_save = 1
```

# Regex for camelCase detection

```
# vim regex
\v(\a|\d)+(\u(\l|\d)+|\u@<!\u+)(\w)@!

# python regex
[0-9A-Za-z]+(?:[A-Z][a-z0-9]+|(?<![A-Z])[A-Z]+)(?!\w)

# Following words are camelcase
PescalXXXCase
cemelXXXCase
XXXPescalCase
XXXcemelCase
I18Word
pescalCASE
cemelCASE

# Following words are not camelcase
CEMEL_CASE
CEMEL
snek_case
Snekcase
Snek_case
```

## TODO

- Jump to errors highlighted by camelspell
- Clear mistakes when buffer is closed ``BufDelete``
- Calculate spell mistake highlights when new word is added
