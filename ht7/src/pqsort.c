#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include "../include/taskqueue.h"
#include "../include/pqsort.h"
#include "time.h"

static volatile int progress = 0;

void thpool_init(threadpool_t* pool, size_t thread_number){
    init_queue(&pool->tasks);
    pool->threads = malloc(thread_number*sizeof(pthread_t));
    pool->thread_number = thread_number;
    pthread_mutex_init(&pool->mutex, NULL);
    pthread_cond_init(&pool->cond, NULL);
}

void free_threadpool(threadpool_t* pool){
    free(pool->threads);
    free_queue(&pool->tasks);
}

void thpool_submit(threadpool_t* pool, task_t* task){
    queue_push(&pool->tasks, *task);
}
    
void sort_part(void* data){
    taskargs_t* args;
    args = (taskargs_t*) data;
    size_t size;
    size = args->end - args->begin;
    if (size <= 1){
        pthread_mutex_lock(&args->pool->mutex);
        progress -= 1;
        pthread_mutex_unlock(&args->pool->mutex);
    }
    else{
        task_t new_task;
        int x;
        x = rand()%size;
        int* ind = partition(args->begin, args->end - 1, *(args->begin + x));
        pthread_mutex_lock(&args->pool->mutex);
        add_task(&new_task, args->pool, args->begin, ind + 1);
        add_task(&new_task, args->pool, ind + 1, args->end);
        pthread_mutex_unlock(&args->pool->mutex);
    }
}

int* partition(int* l, int* r, int x){
    while (l <= r){
        while(*l < x) l++;
        while(*r > x) r--;
        if (l <= r){
            int tmp = *l;
            *(l++) = *r;
            *(r--) = tmp;
        }
    }
    return r;
}

void add_task(task_t* task, threadpool_t* pool, int* begin, int* end){
        taskargs_t* args = malloc(sizeof(taskargs_t));
        args->pool = pool;
        args->begin = begin;
        args->end = end;
        init_task(task, sort_part, args);
        thpool_submit(pool, task);    
}

void wait_task(threadpool_t* pool){
	if (!pool->tasks.size)
		pthread_cond_wait(&pool->cond, &pool->mutex);
}

void* go(void* arg){
    threadpool_t* pool = (threadpool_t*) arg;
    while (1){
        int rc = 0;
        task_t task;
        pthread_mutex_lock(&pool->mutex);
        if (progress == 0){
            pthread_mutex_unlock(&pool->mutex);
            break;    
        }
        wait_task(pool);
        if (pool->tasks.size > 0){
            task = queue_pop(&pool->tasks);
            rc = 1;
        }
        pthread_mutex_unlock(&pool->mutex);
        if (rc){
            task_run(&task);
            free_task(&task);
        }
    }
    return NULL;
}

void thpool_finit(threadpool_t* pool){
    size_t i;
    for (i = 0; i < pool->thread_number; i++)
		pthread_join(*(pool->threads + i), NULL);
    pthread_mutex_destroy(&pool->mutex);
    pthread_cond_destroy(&pool->cond);
}

void sort(threadpool_t* pool){
    size_t i;
    for (i = 0; i < pool->thread_number; i++)
        pthread_create(pool->threads + i, NULL, go, pool);     
}

int main()
{
    srand(time(NULL));
    int n = 10;
    progress = n;
    int* array = malloc(sizeof(int)*n);    
	int i;
	threadpool_t pool;
    task_t task;
	for (i = 0; i < n; i++)
	    array[i] = rand()%15;
	thpool_init(&pool, 5);
    taskargs_t* args = malloc(sizeof(taskargs_t));
    args->pool = &pool;
    args->begin = array;
    args->end = array + n;
    init_task(&task, sort_part, args);
    thpool_submit(&pool, &task);
    sort(&pool);
    thpool_finit(&pool);
    free_threadpool(&pool);
	for (i = 0; i < n; i++)
	    printf("%d ", array[i]);
	free(array);
	return 0;
}



