from threading import Thread, Condition
from queue import Queue
from time import sleep
import signal, os


cnt = 0

exit_flag = 0

cv = Condition()
q = Queue()



def draw():
    global exit_flag
    while True:
        with cv:

            while q.empty():
                cv.wait()

            mytmp = q.get_nowait()
            try:
                if mytmp == 6:
                    exit_flag = 1
                    print("exit thread")
                    break
                print(f"q value: {mytmp}")
            except:
                pass

            sleep(0.1)

def read_to_queue():
    global cnt
    global exit_flag

    print("ff")

    cnt += 1
    q.put(cnt)

    sleep(3)
    with cv:
        cv.notify_all()


        
def int_handler(signum, frame):
    global  exit_flag
    exit_flag = 1
    q.put(6)
    with cv:
        cv.notify_all()


def read_serial():
    
    read_to_queue()
    Thread(target=draw).start()

    while(not exit_flag):
        read_to_queue()


signal.signal(signal.SIGINT, int_handler)
read_serial()



'''
def oreder_proc(name):
    while True:
        with cv:
            while q.empty():
                cv.wait()

            try:
                order = q.get_nowait()
                print(f"{name}: {order}")
                
                if order == "stop":
                        break
            except:
                pass

            sleep(0.5)

Thread(target=oreder_proc, args=("thread 1",)).start()
Thread(target=oreder_proc, args=("thread 2",)).start()
Thread(target=oreder_proc, args=("thread 3",)).start()


# Put data into queue
for i in range(10):
   q.put(f"order {i}")
# Put stop-commands for consumers
for _ in range(3):
   q.put("stop")
# Notify all consumers
with cv:
   cv.notify_all()
'''