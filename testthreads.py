import threading
import time

import ttyio5 as ttyio

idlecounter = 0
def run_thread():
    while True:
        print('thread running')
        time.sleep(1)
        global stop_threads
        if stop_threads:
            break
        global idlecounter
        idlecounter += 1
        if idlecounter > 5:
            stop_threads = True
            break

stop_threads = False
t1 = threading.Thread(target=run_thread)
t1.start()
# time.sleep(0.25)

q = ''
while q != 'q':
    q = ttyio.getch() # input()

stop_threads = True
t1.join()
print('finish')