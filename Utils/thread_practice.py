import logging
import threading
import time

def thread_function(var01):
    for i in range(10):
        print(var01, i)
        time.sleep(1)

t1 = threading.Thread(target=thread_function, args=(1,))
t2 = threading.Thread(target=thread_function, args=(2,))

t1.start()
t2.start()