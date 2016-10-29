CFLAGS  ?= -Wall -Wextra -Werror -ansi -pedantic
LDFLAGS ?= -lpthread

all: bin pqsort	
pqsort: bin/taskqueue.o bin/pqsort.o
	gcc bin/pqsort.o bin/taskqueue.o -o pqsort
bin/pqsort.o: src/pqsort.c include/taskqueue.h
	gcc -c src/pqsort.c -o bin/pqsort.o
bin/taskqueue.o: src/taskqueue.c include/taskqueue.h
	gcc -c src/taskqueue.c -o bin/taskqueue.o

bin/util.o: src/util.c include/io.h
	gcc -c src/util.c -o bin/util.o
bin/io.o: src/io.c
	gcc -c src/io.c -o bin/io.o
bin:
	mkdir -p bin
clean:
	rm -r -f bin
