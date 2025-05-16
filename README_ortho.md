# The source files

* `apertium-sgw.post2013-pre2013.lexc` - has alphabet mapping (from post-2013 to pre-2013); currently only one character is converted (ኸ / ሐ )
* `apertium-sgw.post2013-pre2013.twol` - for any rules, if it's more complicated than one-to-one mappings

# The generated files

* `sgw.automorf.hfst` - the regular automorph file now accepts both orthographies:
```
$ echo "አኸ አሐ"  | hfst-proc sgw.automorf.hfst 
^አኸ/አሐ<prn><dem>$ ^አሐ/አሐ<prn><dem>$
```
* `sgw.autogen.hfst` - autogen will only generate post-2013 orthography:
```
$ echo "አሐ<prn><dem>" | hfst-proc sgw.autogen.hfst 
^አሐ<prn><dem>/አሐ$
```
* `sgw@pre2013.autogen.hfst` - for generating pre-2013 orthography:
```
$ echo "አሐ<prn><dem>" | hfst-proc sgw@pre2013.autogen.hfst 
^አሐ<prn><dem>/አኸ$
```
* `sgw@pre2013-sgw@post2013.hfst` - for converting from pre-2013 to post-2013 orthography:
```
$ echo አኸ | hfst-proc -g sgw@pre2013-sgw@post2013.hfst
አሐ   # CURRENTLY NOT WORKING AS EXPECTED
```
* `sgw@post2013-sgw@pre2013.hfst` - for converting from post-2013 to pre-2013 orthography:
```
$ echo አሐ | hfst-proc -g sgw@post2013-sgw@pre2013.hfst
አኸ   # CURRENTLY NOT WORKING AS EXPECTED
```
* `sgw@pre2013-sgw@post2013.bin` - for converting from pre-2013 to post-2013 orthography:
```
$ echo አኸ | lt-proc -t sgw@pre2013-sgw@post2013.bin
አሐ
```
* `sgw@post2013-sgw@pre2013.bin` - for converting from post-2013 to pre-2013 orthography:
```
$ echo አሐ | lt-proc -t sgw@post2013-sgw@pre2013.bin
አኸ
```

# Added modes
* `sgw-morph` now analyses both orthographies
* `sgw-gener` only generates post-2013 orthography
* `sgw_pre2013-gener` generates pre-2013 orthography
```
$ echo "^አሐ<prn><dem>$" | apertium -d . -f none sgw_pre2013-gener
አኸ
```
* `sgw_post2013-sgw_pre2013` and `sgw_pre2013-sgw_post2013` do orthography conversion
```
$ echo አሐ | apertium -d . -f none sgw_post2013-sgw_pre2013
^አሐ/አኸ$
```

# TODO
In order for all the above to work as described:
* convert main lexicon (lexd) file to post-2013 orthography
* complete the orthographic mapping in the new source files ([#The source files])
* you'll need some sort of evaluation of effectiveness
