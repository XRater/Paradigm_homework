#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include "../include/taskqueue.h"


/*
typedef struct ThreadPool{
    queue_t tasks;
    pthread_t* threads;
    size_t maxtask;
    size_t task_number;
    size_t thread_number;
} threadpool_t;    

void thpool_init(threadpool_t* pool, size_t array_size, size_t thread_number){
    init_queue(&pool->tasks);
    pool->threads = malloc(thread_number*sizeof(pthread_t));
    pool->maxtask = array_size;
    pool->thread_number = thread_number;
    pool->task_number = 0;
}

void free_threadpool(threadpool_t* pool){
    free(pool->threads);
}

void thpool_submit(threadpool_t* pool, task_t* task){
    queue_push(&pool->tasks, task);
    pool->task_number++;
}
*/
/*
void work(threadpool_t* pool){
    
}
*/
/*
void thsort(threadpool_t* pool){
    while (pool->thread_number){
        queue_run(&pool->tasks);    
    }
}

void print(threadpool_t* pool, int* a, size_t size){
    if (size == 1)
        printf("%d", *a);
    else{
        
    }
}
*/

void printcall(int number){
    printf("Called%d\n", number);
}

int main()
{
    int n = 4;
    int* array = malloc(sizeof(int)*4);    
	int i;
//	threadpool_t pool;
    task_t task1, task2;
	for (i = 0; i < n; i++){
	    array[i] = i;
	}
//	thpool_init(&pool, 4, 10);
    queue_t queue;
    int* args[2] = {array, array + 1};
    task1.args = args;
    task1.func = printcall;
    task2.args = args;
    task2.func = printcall;
    task2.number = 2;
    task1.number = 1;
    init_queue(&queue);
    queue_push(&queue, task1);
    queue_push(&queue, task2);
    //printf("%d", (int)queue.size);
    queue_run(&queue);
    queue_pop(&queue);
    queue_run(&queue);
    free_queue(&queue);
//    thpool_submit(&pool, &task);
//    thsort(&pool);
//    free_threadpool(&pool);
	free(array);
	return 0;
}



