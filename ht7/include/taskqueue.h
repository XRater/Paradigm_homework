#ifndef __QUEUE_H__
#define __QUEUE_H__
#include <stdlib.h>

typedef struct Task{
    void (*func)();
    void* args;
    int number;
} task_t;    

typedef struct QNode{
    task_t task;
    struct QNode* next;
    struct QNode* prev;
} qnode_t;

typedef struct Queue{
    size_t size;
    qnode_t head;
} queue_t;

void init_qnode(qnode_t* node, task_t task);
void init_queue(queue_t* queue);
void queue_push_node(queue_t* queue, qnode_t* node);
void queue_push(queue_t* queue, task_t task);
task_t queue_pop(queue_t* queue);
void task_run(task_t task);
void queue_run(queue_t* queue);
void free_queue(queue_t* queue);

#endif 
