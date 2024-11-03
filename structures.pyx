cdef extern from "stdlib.h":
    void* malloc(size_t size)
    void free(void* ptr)

cdef struct node:
    int val
    node* next

ctypedef node slnode

cdef slnode *start = NULL
cdef slnode *last = NULL
cdef slnode *temp

cdef append(int num):
    global start, last
    temp = <slnode*> malloc(sizeof(slnode*))
    if start == NULL:
        start = last = temp
    else:
        last.next = temp
        last = temp

cpdef display():
    if start == NULL:
        print("No element to display")
    else:
        temp = start
        while temp != NULL:
            print(temp.val)
            temp = temp.next