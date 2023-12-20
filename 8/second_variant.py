import threading
import time

def print_messages(thread_number):
    for i in range(5):
        time.sleep(1)
        print(f"Сообщение от потока {thread_number}: {i}")

thread1 = threading.Thread(target=print_messages, args=(1,))
thread2 = threading.Thread(target=print_messages, args=(2,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()
