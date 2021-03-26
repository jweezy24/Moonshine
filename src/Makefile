CC=gcc
CFLAGS = -Wall
BIN = ../bin
TARGET = Moonshine

OBJS = main.o numutils.o

all: Moonshine

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

install:
	mkdir -p $(BIN)
	cp $(TARGET) $(BIN)

clean:
	rm -f $(OBJS) $(TARGET)

