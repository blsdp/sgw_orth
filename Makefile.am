###############################################################################
## Makefile for apertium-sgw
###############################################################################

LANG1=sgw
SCRIPT1=post2013
SCRIPT2=pre2013
LANG1SCRIPT1=sgw@$(SCRIPT1)
LANG1SCRIPT2=sgw@$(SCRIPT2)
BASENAME=apertium-$(LANG1)

TARGETS_COMMON =			\
	$(LANG1).automorf.hfst		\
	$(LANG1).automorf.bin		\
	$(LANG1).automorf.att.gz	\
	$(LANG1).autogen.hfst		\
	$(LANG1SCRIPT2).autogen.hfst		\
	$(LANG1).autogen.bin		\
	$(LANG1SCRIPT2).autogen.bin		\
	$(LANG1).autogen.att.gz		\
	$(LANG1).autopgen.bin		\
	$(LANG1).rlx.bin \
	$(LANG1SCRIPT1)-$(LANG1SCRIPT2).hfst \
	$(LANG1SCRIPT2)-$(LANG1SCRIPT1).hfst \
	$(LANG1SCRIPT1)-$(LANG1SCRIPT2).bin \
	$(LANG1SCRIPT2)-$(LANG1SCRIPT1).bin


if ENABLE_SPELLER
TARGETS_COMMON += $(LANG1).zhfst
endif

# This include defines goals for install-modes, .deps/.d, autobil.prefixes and .mode files:
@ap_include@



if ENABLE_LINTER
TARGETS_COMMON += lint
endif

.PHONY: lint

lint:
	apertium-lint

###############################################################################
## Sebat Bet Gurage transducer
###############################################################################

.deps/$(LANG1).twol.hfst: $(BASENAME).$(LANG1).twol .deps/.d
	hfst-twolc $< -o $@

.deps/$(LANG1).RL.lexd: $(BASENAME).$(LANG1).lexd .deps/.d
	cat $< | grep -v 'Dir/LR' > $@

.deps/$(LANG1).LR.lexd: $(BASENAME).$(LANG1).lexd .deps/.d
	cat $< | grep -v 'Dir/RL' > $@

.deps/$(LANG1).RL.lexd.hfst: .deps/$(LANG1).RL.lexd
	lexd $< .deps/$(LANG1).RL.lexd.att
	hfst-txt2fst .deps/$(LANG1).RL.lexd.att -o $@

.deps/$(LANG1).LR.lexd.hfst: .deps/$(LANG1).LR.lexd
	lexd $< .deps/$(LANG1).LR.lexd.att
	hfst-txt2fst .deps/$(LANG1).LR.lexd.att -o $@


.deps/$(LANG1).RL.hfst: .deps/$(LANG1).RL.lexd.hfst .deps/$(LANG1).twol.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).RL.lexd.hfst -2 .deps/$(LANG1).twol.hfst -o $@

.deps/$(LANG1).LR.hfst: .deps/$(LANG1).LR.lexd.hfst .deps/$(LANG1).twol.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).LR.lexd.hfst -2 .deps/$(LANG1).twol.hfst -o $@

$(LANG1).autogen.hfst: .deps/$(LANG1).RL.hfst
	hfst-fst2fst -O $< -o $@

.deps/$(LANG1).spellrelax.hfst: $(BASENAME).$(LANG1).spellrelax .deps/.d
	hfst-regexp2fst -S -o $@ $<

# primary script (post2013) analyser
.deps/$(LANG1SCRIPT1).automorf.hfst: .deps/$(LANG1).LR.hfst .deps/$(LANG1).spellrelax.hfst
	hfst-compose -1 $< -2 .deps/$(LANG1).spellrelax.hfst | hfst-invert -o $@ # | hfst-fst2fst -O -o $@

# secondary script (pre2013) analyser
.deps/$(LANG1SCRIPT2).automorf.hfst: .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).hfst .deps/$(LANG1).LR.hfst .deps/$(LANG1).spellrelax.hfst
	hfst-compose -1 `echo $(word 2,$^)` -2 $< | hfst-compose-intersect -1 - -2 `echo $(word 3,$^)` | hfst-invert -o $@

# The final analyser is a combinaton of the normative analyser (pre2013) and the secondary script analyser (post2013)
$(LANG1).automorf.hfst: .deps/$(LANG1SCRIPT1).automorf.hfst .deps/$(LANG1SCRIPT2).automorf.hfst
	hfst-invert $< -o .deps/$(LANG1SCRIPT1).REVautomorf.hfst
	hfst-invert `echo $(word 2,$^)` -o .deps/$(LANG1SCRIPT2).REVautomorf.hfst
	hfst-union -1 .deps/$(LANG1SCRIPT1).REVautomorf.hfst -2 .deps/$(LANG1SCRIPT2).REVautomorf.hfst | hfst-invert | hfst-minimise | hfst-fst2fst -w -o $@

$(LANG1).autogen.att.gz: $(LANG1).autogen.hfst
	hfst-fst2txt $< | gzip -9 -c -n > $@

$(LANG1).automorf.att.gz: $(LANG1).automorf.hfst
	hfst-fst2txt $< | gzip -9 -c -n > $@

$(LANG1).autogen.bin: $(LANG1).autogen.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).autogen.att
	lt-comp lr .deps/$(LANG1).autogen.att $@

$(LANG1).automorf.bin: $(LANG1).automorf.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1).automorf.att
	lt-comp lr .deps/$(LANG1).automorf.att $@

$(LANG1).autopgen.bin: $(BASENAME).post-$(LANG1).dix
	lt-comp lr $< $@

#### Orthography conversion ####

# compile the first stage of the pre2013-post2013 transliteration transducer
.deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).lexc.hfst: ./$(BASENAME).$(SCRIPT1)-$(SCRIPT2).lexc
	hfst-lexc $< -o $@

# compile the second stage of the pre2013-post2013 transliteration transducer
.deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).twol.hfst: ./$(BASENAME).$(SCRIPT1)-$(SCRIPT2).twol
	hfst-twolc $< -o $@

# compile the transliteration transducer
.deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).hfst: .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).twol.hfst .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).lexc.hfst
	hfst-compose-intersect -1 `echo $(word 2,$^)` -2 $< -o $@

.deps/$(LANG1SCRIPT2)-$(LANG1SCRIPT1).hfst: .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).hfst
	hfst-invert $< -o $@

# orthography conversion modes
$(LANG1SCRIPT1)-$(LANG1SCRIPT2).hfst: .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).hfst
	hfst-fst2fst $< -w -o $@

$(LANG1SCRIPT2)-$(LANG1SCRIPT1).hfst: .deps/$(LANG1SCRIPT2)-$(LANG1SCRIPT1).hfst
	hfst-fst2fst $< -w -o $@

$(LANG1SCRIPT1)-$(LANG1SCRIPT2).bin: .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).hfst
	hfst-minimise $< | hfst-fst2txt -o .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).att
	lt-comp lr .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).att $@

$(LANG1SCRIPT2)-$(LANG1SCRIPT1).bin: .deps/$(LANG1SCRIPT2)-$(LANG1SCRIPT1).hfst
	hfst-minimise $< | hfst-fst2txt -o .deps/$(LANG1SCRIPT2)-$(LANG1SCRIPT1).att
	lt-comp lr .deps/$(LANG1SCRIPT2)-$(LANG1SCRIPT1).att $@


#### pre-2013 generation ####

$(LANG1SCRIPT2).autogen.hfst: .deps/$(LANG1SCRIPT1)-$(LANG1SCRIPT2).hfst .deps/$(LANG1).RL.hfst
	hfst-compose -1 `echo $(word 2,$^)` -2 $< | hfst-fst2fst -w -o $@

$(LANG1SCRIPT2).autogen.att.gz: $(LANG1SCRIPT2).autogen.hfst
	hfst-fst2txt $< | gzip -9 -c -n > $@

$(LANG1SCRIPT2).autogen.bin: $(LANG1SCRIPT2).autogen.att.gz .deps/.d
	zcat < $< > .deps/$(LANG1SCRIPT2).autogen.att
	lt-comp lr .deps/$(LANG1SCRIPT2).autogen.att $@


###############################################################################
## Debugging transducers (for testvoc)
###############################################################################


debug: .deps/$(LANG1).LR-debug.hfst .deps/$(LANG1).lexd.hfst


.deps/$(LANG1).LR-debug.hfst: $(BASENAME).$(LANG1).lexd .deps/.d
	cat $< | grep -v 'Dir/RL' | grep -v 'Use/Circ' > .deps/$(LANG1).LR-debug.lexd
	lexd .deps/$(LANG1).LR-debug.lexd .deps/$(LANG1).LR-debug.lexd.att
	hfst-txt2fst .deps/$(LANG1).LR-debug.lexd.att -o .deps/$(LANG1).LR-debug.lexd.hfst
	hfst-compose-intersect -1 .deps/$(LANG1).LR-debug.lexd.hfst -2 .deps/$(LANG1).twol.hfst -o $@

.deps/$(LANG1).lexd.hfst: .deps/$(LANG1).RL.lexd.hfst
	hfst-fst2fst -O -i $< -o $@
###############################################################################
## Disambiguation rules
###############################################################################

$(LANG1).rlx.bin: $(BASENAME).$(LANG1).rlx
	cg-comp $< $@

###############################################################################
## Spell checker
###############################################################################

$(LANG1).zhfst: .deps/acceptor.default.hfst .deps/errmodel.default.hfst speller/index.xml
	rm -f $@
	zip -j $@ $^

.deps/editdist.default.att: speller/editdist.default.txt .deps/acceptor.default.hfst
	apertium-editdist -v -s -d 1 -e '@0@' -i $(srcdir)/speller/editdist.default.txt -a .deps/acceptor.default.hfst > $@

.deps/editdist.default.hfst: .deps/editdist.default.att
	hfst-txt2fst -e '@0@' $< -o $@

.deps/editstrings.default.hfst: .deps/strings.default.hfst .deps/editdist.default.hfst
	hfst-disjunct $^ | hfst-minimise | hfst-repeat -f 1 -t 2 -o $@

.deps/errmodel.default.hfst: .deps/words.default.hfst .deps/editstrings.default.hfst
	hfst-disjunct $^ | hfst-fst2fst -f olw -o $@

.deps/words.default.hfst: speller/words.default.txt
	grep -v -e "^#" -e "^$$" $< | hfst-strings2fst  -j -o $@

.deps/strings.default.hfst: speller/strings.default.txt .deps/anystar.hfst
	grep -v -e "^#" -e "^$$" $< | hfst-strings2fst  -j | hfst-concatenate .deps/anystar.hfst - |\
	hfst-concatenate - .deps/anystar.hfst -o $@

.deps/anystar.hfst:
	echo "?*;" | hfst-regexp2fst -S -o $@

.deps/acceptor.default.hfst: $(LANG1).autogen.hfst
	cat $< | hfst-fst2fst -t | hfst-project --project=lower | hfst-minimise | hfst-fst2fst  -f olw -o $@


###############################################################################
## Unigram tagger
###############################################################################

#$(LANG1).prob: corpus/$(LANG1).tagged
#	apertium-tagger -s 0 -u 2 $@ $<

###############################################################################
## Distribution
###############################################################################

EXTRA_DIST= \
		$(BASENAME).$(LANG1).lexd	\
		$(BASENAME).$(LANG1).twol	\
		$(BASENAME).$(LANG1).rlx	\
		$(BASENAME).post-$(LANG1).dix	\
		$(LANG1).prob			\
		modes.xml

###############################################################################
## Installation stuff
###############################################################################
#
#   apertium_sgw_dir: This is where the compiled binaries go
#   apertium_sgw_srcdir: This is where the source files go

apertium_sgwdir=$(prefix)/share/apertium/$(BASENAME)/
apertium_sgw_srcdir=$(prefix)/share/apertium/$(BASENAME)/

apertium_sgw_DATA=$(TARGETS_COMMON) \
	$(BASENAME).$(LANG1).lexd	\
	$(BASENAME).$(LANG1).twol	\
	$(BASENAME).$(LANG1).rlx	\
	$(BASENAME).post-$(LANG1).dix	\
	$(LANG1).prob

pkgconfigdir = $(prefix)/share/pkgconfig
pkgconfig_DATA = $(BASENAME).pc

noinst_DATA=modes/$(LANG1)-morph.mode

install-data-local: install-modes
uninstall-local: uninstall-modes

###############################################################################
## Cleanup
###############################################################################

CLEANFILES = $(TARGETS_COMMON)
clean-local:
	-rm -rf .deps modes

###############################################################################
## Test
###############################################################################

test: all
	apertium-regtest test
