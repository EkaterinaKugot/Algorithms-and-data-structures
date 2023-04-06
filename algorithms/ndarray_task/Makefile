CC = g++
CFLAGS = -std=c++17 -Wall -pedantic
SOURCES = main.cpp

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
	./$(TARGET)
	
