# poeditHelper
script to help two or more editors work with poedit translations
it parses .po format and shows some statistics.

usage: 
1. poeditHelper file.po
will report length of all translated original text, and echo this text itself.
will report length of all not translated original text and echo this text itself.

2. poeditHelper file1.po file2.po
will report length of original text, which translation differs in file2.po.

