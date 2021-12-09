CXX = g++-10
CXXFLAGS = -g -O2 -std=c++20 -Wall -Wextra

BUILD = build

SRC = $(sort $(wildcard *.cpp))
EXE = $(SRC:%.cpp=build/%)

all: $(EXE) | $(BUILD)

clean:
	$(RM) -fr $(BUILD) core *~

run: $(EXE)
	@for x in $(EXE); do echo "[Day $$(basename $$x)]"; $$x; echo; done

$(BUILD)/% : %.cpp aoc.hpp | $(BUILD)
	$(LINK.cc) -o $@ $<

$(BUILD):
	mkdir -p $(BUILD)
