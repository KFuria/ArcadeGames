CC = gcc
OPT = -O3
LIBS = -lmingw32 -lSDL2main -lSDL2
CFLAGS = -Wall -Wextra -g -std=c99 $(OPT) -pedantic
MAIN = snake

SRC_FILES = $(wildcard *.c)
OBJS_FILES = $(SRC_FILES:.c=.o)

all: $(MAIN)

$(MAIN): $(OBJS_FILES)
	$(CC) $(CFLAGS) -o $(MAIN).exe $(OBJS_FILES) $(LIBS)

.c.o:
	$(CC) $(CFLAGS) -c $< -o $@

clean: 
	$(RM) *.o *~ $(MAIN).exe


