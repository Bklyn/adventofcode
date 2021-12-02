CXX = g++ -std=c++20
CXXFLAGS = -g -O2

BUILD = build

SRC = $(wildcard *.cpp)
EXE = $(SRC:%.cpp=build/%)

all: $(EXE)

clean:
	$(RM) -fr $(BUILD)

$(BUILD)/% : %.cpp | $(BUILD)
	$(LINK.cc) -o $@ $<

$(BUILD):
	@mkdir -p $(BUILD)
