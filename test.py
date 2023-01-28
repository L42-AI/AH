from multiprocessing import Process, Queue
import time

def multiprocessor(queue):
    while True:
        print('yes')
        # time.sleep(1)
        data = "data"
        queue.put(data)

def gui(queue):
    while True:
        print('Yes')
        data = queue.get()
        print(data)


if __name__ == "__main__":
    queue = Queue()

    multiprocessor_process = Process(target=multiprocessor, args=(queue,))
    multiprocessor_process.start()

    gui_process = Process(target=gui, args=(queue,))
    gui_process.start()

    multiprocessor_process.join()
    gui_process.join()

