#include "../include/taskqueue.h"
#include <stdlib.h>

void init_qnode(qnode_t* node, task_t task){
    node->next = NULL;
    node->prev = NULL;
    node->task = task;
}

void init_queue(queue_t* queue){
    queue->size = 0;
    queue->head.next = &queue->head;
    queue->head.prev = &queue->head;
}

void queue_push_node(queue_t* queue, qnode_t* node){
    node->next = &queue->head;
    node->prev = queue->head.prev;
    queue->head.prev->next = node;
    queue->head.prev = node;
    queue->size++; 
}

void queue_push(queue_t* queue, task_t task){
    qnode_t* node = malloc(sizeof(qnode_t));
    init_qnode(node, task);
    queue_push_node(queue, node);
}

task_t queue_pop(queue_t* queue){
    qnode_t* node = queue->head.next;
    queue->head.next->next->prev = &queue->head;
    queue->head.next = queue->head.next->next;
    task_t task = node->task;
    queue->size--;
    free(node);
    return task;
}

void task_run(task_t* task){
    task->func(task->args);
}

void init_task(task_t* task, void (*func)(), void* data){
    task->func = func;
    task->args = data;
}

void free_task(task_t* task){
    free(task->args);
}


void queue_run(queue_t* queue){
    qnode_t* node = queue->head.next;
    while (&queue->head != node){
        task_run(&(node->task));
        node = node->next;
    }
}

void free_queue(queue_t* queue){
    qnode_t* node = queue->head.next;
    while (&queue->head != node){
        node = node->next;
        free_task(&node->prev->task);
        free(node->prev);
    }
}

