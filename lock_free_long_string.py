"""
Write a program using optimistic lock to fix race-condition

Steps: 
I. create a race-condition code by using multiprocessing + shared memory (*a*:Array) https://docs.python.org/2/library/multiprocessing.html
expected first output: [1,0,0,1] or [0,2,0,2] => got: [1,2,1,2]

II. write lock-free(fake) code base on optimistic locking principle.
1. Using *key*:Value as a version of current *a*:Array
2. create new array *b* with the value copy from *a* and *key_b* copy from *key*
3. change on new array b
4. when finish, check if *key* == *key_b* => change on *a* and increase *key* by 1. If *key* != *key_b*, retry

"""

""" Race-condition code

from multiprocessing import Process, Value, Array
import os
import random


def transaction(key, a, value):

    for i in range(len(a)):
        x = random.randint(0, len(a)-1)
        a[x] = value
    
    print('---a', a[:])
    print('---process', os.getpid())


if __name__ == '__main__':
    # Using Value and Array type to push value in the same shared memory map between process
    key = Value('i', 1)
    arr = Array('i', range(100))
    for i in range(len(arr)):
        arr[i] = 0

    p1 = Process(target=transaction, args=(key, arr, 1))
    p2 = Process(target=transaction, args=(key, arr, 2))
    p3 = Process(target=transaction, args=(key, arr, 3))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    print(arr[:])
""" 

""" Lock-free FAKE =))))
from multiprocessing import Process, Value, Array
import os
import random

def compare_and_swap(x, y):
    if x != y:
        return False
    return True


def transaction(key, a, value, retry_time):
    print(f'-------key: {key.value}, value: {value}, retry: {retry_time}')
    if retry_time > 3:
        print('Maximum retry_times error: process', os.getpid())
        return 


    # copy a and key
    b = Array('i', range(len(a)))
    key_b = Value('i', key.value)
    for i in range(len(b)):
        b[i] = a[i]

    # change on b
    for i in range(len(b)):
        x = random.randint(0, len(a)-1)
        b[x] = value
    
    # apply to a
    print(f'checking.... key={key.value} and key_b={key_b.value} of process {os.getpid()} with value={value}')
    if not compare_and_swap(key.value, key_b.value):
        transaction(key, a, value, retry_time+1)
    else:
        key.value = key.value + 1
        for i in range(len(a)):
            a[i] = b[i]
        print(f'with key version {key.value}, a after changing', a[:])
        print(f'finish process', os.getpid())


if __name__ == '__main__':
    # Using Value and Array type to push value in the same shared memory map between process
    key = Value('i', 1)
    arr = Array('i', range(100))
    for i in range(len(arr)):
        arr[i] = 0

    p1 = Process(target=transaction, args=(key, arr, 1, 0))
    p2 = Process(target=transaction, args=(key, arr, 2, 0))
    p3 = Process(target=transaction, args=(key, arr, 3, 0))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
"""

