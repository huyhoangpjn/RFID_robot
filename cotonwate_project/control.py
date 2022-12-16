from threading import Thread
import subprocess
import os

try:
    t1 = Thread(target=subprocess.run, args=(["python", "get_data.py"],))
    t2 = Thread(target=subprocess.run, args=(["python", "main.py"],))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

except KeyboardInterrupt:
    os._exit(0)

