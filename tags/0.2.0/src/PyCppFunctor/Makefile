CXX := g++
CXXFLAGS := -I. -I$(EXTSOFT)/include/python2.3

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -o $@ -c $<

SRCS := $(wildcard ./*.cpp)
OBJS := $(subst .cpp,.o, $(SRCS))


all::	$(OBJS)

debug:
	echo $(OBJS)

clean::
	rm *.o
