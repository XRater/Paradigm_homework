#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include "../include/taskqueue.h"

typedef struct ThreadPool{
    queue_t tasks;
    pthread_t* threads;
    size_t thread_number;
} threadpool_t;    

typedef struct TaskArgs{
    threadpool_t* pool;
    int* begin;
    int* end;
} taskargs_t;

void thpool_init(threadpool_t* pool, size_t thread_number){
    init_queue(&pool->tasks);
    pool->threads = malloc(thread_number*sizeof(pthread_t));
    pool->thread_number = thread_number;
}

void free_threadpool(threadpool_t* pool){
    free(pool->threads);
    free_queue(&pool->tasks);
}

void thpool_submit(threadpool_t* pool, task_t* task){
    queue_push(&pool->tasks, *task);
}
    
void print(void* data){
    taskargs_t* args;
    args = (taskargs_t*) data;
    size_t size;
    size = args->end - args->begin;
    if (size == 1)
        printf("%d", *(args->begin));
    else{
        task_t task_first, task_second;
        add_task(&task_first, args->pool, args->begin, args->begin + size/2);
        add_task(&task_first, args->pool, args->begin + size/2, args->end);
    }
}

void add_task(task_t* task, threadpool_t* pool, int* begin, int* end){
        taskargs_t* args = malloc(sizeof(taskargs_t));
        args->pool = pool;
        args->begin = begin;
        args->end = end;
        init_task(task, print, args);
        thpool_submit(pool, task);    
}


void go(threadpool_t* pool){
    while (pool->tasks.size > 0){
        task_t task = queue_pop(&pool->tasks);
        task_run(&task);
        free_task(&task);
    }
}

/*
void printcall(void* data){
    taskargs_t* args = (taskargs_t*) data;
    printf("Called\n");
}
*/
int main()
{
    int n = 10;
    int* array = malloc(sizeof(int)*n);    
	int i;
	threadpool_t pool;
    task_t task1, task2;
	for (i = 0; i < n; i++){
	    array[i] = i;
	}
	thpool_init(&pool, 1);
    taskargs_t* args = malloc(sizeof(taskargs_t));
    args->pool = &pool;
    args->begin = array;
    args->end = array + n;
    init_task(&task1, print, args);
    thpool_submit(&pool, &task1);
    //task_t task = queue_pop(&pool.tasks);
    //task_run(&task);
    go(&pool);
    free_threadpool(&pool);
	free(array);
	return 0;
}



