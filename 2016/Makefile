PYTHON  = python
SCRIPTS = $(wildcard *.py)
ANSWERS = $(subst .py,.ans,$(SCRIPTS))

.SUFFIXES: .ans

all: $(ANSWERS)

clean:
	$(RM) *.ans *~

%.ans: %.py
	$(PYTHON) $< > $@
