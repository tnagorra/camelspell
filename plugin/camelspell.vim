" Check if python is available
if !has('python3')
  echo 'Error: camelspell requires vim compiled with +python'
  finish
endif

" Import python script
let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')
python3 << EOF
import sys
from os.path import normpath, join
import vim

plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)

import camelspell
EOF

" Set default values
if !exists('g:camelspell_delay')
  let g:camelspell_delay = 300
endif
if !exists('g:camelspell_check_on_startup')
  let g:camelspell_check_on_startup = 1
endif
if !exists('g:camelspell_check_on_text_change')
  let g:camelspell_check_on_text_change = 1
endif
if !exists('g:camelspell_check_on_save')
  let g:camelspell_check_on_save = 1
endif

" Local timer_id for s:SpellCheck
let s:timer_id = 0

function! CamelSpellCheck(id)
  let s:timer_id = a:id
  python3 camelspell.spell_check()
endfunction

function! CamelSpellList()
  python3 camelspell.display_spell_errors()
endfunction

function! s:DelayedSpellCheck()
  if s:timer_id
    call timer_stop(s:timer_id)
  endif
  call timer_start(g:camelspell_delay, function('CamelSpellCheck'))
endfunction

set spell
highlight link CamelCaseError SpellBad

" Ignore CamelCase words when spell checking
function! IgnoreCamelCaseSpell()
  syn match CamelCase '\([a-z0-9]\+\)\?\([A-Z]\+[a-z0-9]\+\)\+' contains=@NoSpell transparent
  syn cluster Spell add=CamelCase
endfun

augroup spellcheckcloack
  autocmd!
  autocmd BufRead,BufNewFile * :call IgnoreCamelCaseSpell()
augroup END

augroup spellcheck
  autocmd!
  if camelspell_check_on_startup
    autocmd BufRead * :call CamelSpellCheck(0)
  endif
  if camelspell_check_on_text_change
    autocmd TextChangedI * :call s:DelayedSpellCheck()
    autocmd TextChanged * :call s:DelayedSpellCheck()
  endif
  if g:camelspell_check_on_save
    autocmd BufWrite * :call s:DelayedSpellCheck()
  endif
augroup END
