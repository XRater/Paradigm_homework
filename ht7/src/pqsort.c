#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include "../include/taskqueue.h"
#include "../include/pqsort.h"
#include "time.h"

static volatile int progress = 0;
static int max_depth = 0;


int comp(const void* a, const void* b){
    return (*(int*) a - *(int*) b);
}


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
	pthread_cond_signal(&pool->cond);
}
    
void sort_part(void* data){
    taskargs_t* args = (taskargs_t*) data;
    size_t size;
    size = args->end - args->begin;
    if (size <= 1){
        pthread_mutex_lock(&args->pool->mutex);
        progress -= 1;
        if (progress == 0)
        	pthread_cond_broadcast(&args->pool->cond);
        pthread_mutex_unlock(&args->pool->mutex);
    }
    else{
        if (args->depth > max_depth){
            int n = args->end - args->begin;
            qsort(args->begin, n, sizeof(int), comp);
            progress -= n;
        }
        else{
            task_t new_task;
            int x = rand()%size;
            int* ind = partition(args->begin, args->end - 1, *(args->begin + x));
            pthread_mutex_lock(&args->pool->mutex);
            add_task(&new_task, args->pool, args->begin, ind + 1, args->depth + 1);
            add_task(&new_task, args->pool, ind + 1, args->end, args->depth + 1);
            pthread_mutex_unlock(&args->pool->mutex);
        }
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

void add_task(task_t* task, threadpool_t* pool, int* begin, int* end, int depth){
        if (end - begin > 0){
            taskargs_t* args = malloc(sizeof(taskargs_t));
            args->pool = pool;
            args->begin = begin;
            args->end = end;
            args->depth = depth;
            init_task(task, sort_part, args);
            thpool_submit(pool, task);
        }    
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

int main(int argc, char** argv)
{
//Get parametrs
    if (argc != 4){
        printf("Wrong input format");
        return 1;
    }
    int n = atoi(argv[2]);
    int thread_number = atoi(argv[1]);
//Init variables   
    int* array = malloc(sizeof(int)*n);    
	int i;
	threadpool_t pool;
    task_t task;
    taskargs_t* args = malloc(sizeof(taskargs_t));
//Set arguments    
    max_depth = atoi(argv[3]);
    args->pool = &pool;
    args->begin = array;
    args->end = array + n;
    args->depth = 0;
    init_task(&task, sort_part, args);
    srand(time(NULL));
    progress = n;
	for (i = 0; i < n; i++)
	    array[i] = rand()%15;
//Init thread)pool
	thpool_init(&pool, thread_number);
    thpool_submit(&pool, &task);
//Sort
    sort(&pool);
//Free memory
    thpool_finit(&pool);
    free_threadpool(&pool);
//	for (i = 0; i < n; i++)
//	    printf("%d ", array[i]);
	free(array);
	return 0;
}

