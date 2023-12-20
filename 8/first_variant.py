from threading import Thread
from time import sleep, perf_counter

def task():
    print("Starting doing something ...")
    sleep(1)
    print("Task is done!")

start_time = perf_counter()

t1 = Thread(target=task)
t2 = Thread(target=task)

t1.start()
t2.start()

t1.join()
t2.join()

end_time = perf_counter()

print(f'Time of solving task is >> {end_time - start_time:0.3f} seconds')
