# from tkinter import *

from time import time
import time

# ws = Tk()

# button1 = Button(ws, text = 'Click Here')
# button1.pack(side = TOP, pady = 5)

# print('Welcome to Python Guides Tutorial')

# start = time()

# ws.after(20000, ws.destroy)

# ws.mainloop()

# end = time()
# print('Destroyed after % d seconds' % (end-start))

from random import randint

data = ["test","test","test","test","test",0,"test"]
while True:
    value = randint(0,100)
    data[5]= value
    print(data)
    time.sleep(2)