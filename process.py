from collections import deque
import uuid
import time
from threading import Thread, Event
import multiprocessing
from multiprocessing.pool import ThreadPool

class UID_Process:
    def __init__(self, tracking_id = None):
        self.pid = uuid.uuid4()
        self.tracking_id = tracking_id
        self.begin_time = time.time()
        self.subprocess = ["__init__"]
        print(f"Created Process: {self}")

    def exec_time(self):
        return time.time() - self.begin_time
    
    def create_subprocess(self, identifier):
        self.subprocess.append(identifier)
        print("Create Subprocess ", self, identifier)

    def remove_subprocess(self, identifier):
        self.subprocess.remove(identifier)
        print(f"Remove Subprocess: ", self, identifier)
    
    def __eq__(self, item) -> bool:
        return self.pid == item.pid
    
    def __str__(self):
        return f"{self.pid} - {self.tracking_id}" if not self.subprocess else f"{self.pid} - {self.tracking_id} ({self.subprocess})"

    def __del__(self):
        self.remove_subprocess("__init__")
        print(f"Destroy Process: {self}")

class UID_Queue:
    def __init__(self, name):
        self.name = name
        self.items = deque()
    
    def enqueue(self, process: UID_Process):
        self.items.append(process)
    
    def dequeue(self, process: UID_Process, is_exception=False):
        if not self.is_empty():
            if self.items[0] == process:
                if is_exception:
                    print(f"Exception occurred while processing {process}")
                # print(F"Dequeue achieved {process}")
                return self.items.popleft()
    
    def peek(self):
        return self.items[0]
    
    def is_current(self, process: UID_Process):
        return self.items[0] == process
    
    def is_empty(self):
        return len(self.items) == 0
        
    def size(self):
        return len(self.items)
    
    def process_callback(self, result):
        print(self)
        
    def __str__(self):
        return str([ str(val) for val in self.items])
    
#new addition
q = UID_Queue("Test")

def wait_function_err_exp(length, process_id: UID_Process, identifier: str, started_event=None):
    # print(q)
    while not q.is_current(process_id):
        # print(f"Waiting on {process_id}")
        pass
    try:
        if started_event:
            started_event.set()
        process_id.subprocess(str(identifier))
        # print(process_id)
        time.sleep(length)
        int('s')
    except:
        q.dequeue(process_id, is_exception=True)
    q.dequeue(process_id)
    print("Exiting Func")

def wait_function_exp(length, process_id, started_event=None):
    while not q.is_current(process_id):
        pass
    try:
        if started_event:
            started_event.set()
        time.sleep(length)
    except:
        q.dequeue(process_id, is_exception=True)
    q.dequeue(process_id)

def wait_function_err(length, started_event=None):
    if started_event:
        started_event.set()
    time.sleep(length)
    int('s')

def wait_function(length, started_event=None):
    if started_event:
        started_event.set()
    time.sleep(length)

def main_func():
    p1 = UID_Process("P1")
    q.enqueue(p1)
    try:
        wait_function(1)
    except:
        q.dequeue(p1, is_exception=True)
    q.dequeue(p1)
    print("---------------")
    
    p1_1 = UID_Process("P1-1")
    q.enqueue(p1_1)
    try:
        wait_function_err(1)
    except:
        q.dequeue(p1_1, is_exception=True)
    q.dequeue(p1_1)

def process_init(queue):
    global q
    q = queue


if __name__ == '__main__':
    # Scenario 1
    print("===================================================")
    main_func()
    print("Main Func Complete")

    print("===================================================")
    # Scenario 2
    p2 = UID_Process("P2")
    q.enqueue(p2)
    started_event = Event()
    validator_thread = Thread(target=wait_function_exp, args=(5, p2, started_event))
    validator_thread.start()
    started_event.wait()

    print("---------------")

    p2_2 = UID_Process("P2_2")
    q.enqueue(p2_2)
    started_event = Event()
    validator_thread = Thread(target=wait_function_err_exp, args=(5, p2_2, "thread", started_event))
    validator_thread.start()
    started_event.wait()

    print("===================================================")

    
    # Scenario 4
    p4_4 = UID_Process("P4_4")
    q.enqueue(p4_4)
    while not q.is_current(p4_4):
        pass
    # pool__ = multiprocessing.Pool(processes=2, initializer=process_init, initargs=(q, ))
    pool__ = ThreadPool(processes=2)
    for i in range(0, 1):
        pool__.apply_async(wait_function_err_exp, args=(1, p4_4, str(i)))
    pool__.close()
    pool__.join()
    # print(q)
    q.dequeue(p4_4)

    p4 = UID_Process("P4")
    q.enqueue(p4)
    while not q.is_current(p4):
        pass
    # pool = multiprocessing.Pool(processes=2)
    pool = ThreadPool(processes=2)
    for i in range(0, 5):
        pool.apply_async(wait_function, args=(1,))
    pool.close()
    pool.join()
    q.dequeue(p4)

    print("===================================================")

    # Scenario 3
    print("---------------")
    p3_3 = UID_Process("P3_3")
    q.enqueue(p3_3)
    while not q.is_current(p3_3):
        pass
    pool__ = multiprocessing.Pool(processes=2, initializer=process_init, initargs=(q, ))
    for i in range(0, 1):
        pool__.apply_async(wait_function_err_exp, args=(1, p3_3, str(i)), callback=q.process_callback)
    pool__.close()
    pool__.join()
    # print(q)
    q.dequeue(p3_3)

    p3 = UID_Process("P3")
    q.enqueue(p3)
    while not q.is_current(p3):
        pass
    pool = multiprocessing.Pool(processes=2)
    for i in range(0, 5):
        pool.apply_async(wait_function, args=(1,), callback=q.process_callback)
    pool.close()
    pool.join()
    q.dequeue(p3)

    # print(q)