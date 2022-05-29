import threading
import time

def run_thread():
    while True:
        print('thread running')
        time.sleep(2)
        global stop_threads
        if stop_threads:
            break


stop_threads = False
t1 = threading.Thread(target=run_thread)
t1.start()
time.sleep(0.5)

q = ''
while q != 'q':
    q = input()

stop_threads = True
t1.join()
print('finish')