CC = g++
CFLAGS = -std=c++11 -Wall -pedantic
SOURCES = main.cpp
TARGET2 = main.py

ifeq ($(OS), Windows_NT)
	RM = del
	TARGET = main.exe
else
	RM = rm
	TARGET = main
endif

all:
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCES)

clean:
	echo $(OS)
	$(RM) $(TARGET)

run: all
	.\$(TARGET) | python .\$(TARGET2)
	