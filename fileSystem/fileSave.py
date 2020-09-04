import os
import threading


def SaveFile(name, f):
    with open(name, 'wb+') as destination:
        i = 0
        for chunk in f.chunks():
            destination.write(chunk)
            print("Saving... [" + str(i) + " chunk]")
            i += 1
        print("File saved! [DONE]")

def SaveFileThread(name,f):
    thread = myThread(1, "Saving file", namef=name,  f=f)
    thread.start()


class myThread (threading.Thread):
   def __init__(self, threadID, name, namef, f):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.namef=namef
      self.f=f
   def run(self):
      print ("Starting " + self.name)
      SaveFile(message=self.namef,  f=self.f)
      print ("Exiting " + self.name)