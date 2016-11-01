#ifndef __PQSORT_H__
#define __PQSORT_H__
#include <stdlib.h>

typedef struct ThreadPool{
    queue_t tasks;
    pthread_t* threads;
    size_t thread_number;
    size_t progress;
    pthread_mutex_t mutex;
    pthread_cond_t cond;
} threadpool_t;    

typedef struct TaskArgs{
    threadpool_t* pool;
    int* begin;
    int* end;
} taskargs_t;

void thpool_init(threadpool_t* pool, size_t thread_number);
void free_threadpool(threadpool_t* pool);
void thpool_submit(threadpool_t* pool, task_t* task);
void sort_part(void* data);
void add_task(task_t* task, threadpool_t* pool, int* begin, int* end);
void* go(void* arg);
void* worker(void* args);
void sort(threadpool_t* pool);
int* partition(int* l, int* r, int x);

#endif 
