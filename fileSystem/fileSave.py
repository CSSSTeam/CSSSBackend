import os
import threading


def SaveFile(name, src):
    with open(name, 'wb+') as destination:
        i = 0
        for chunk in f.chunks():
            destination.write(chunk)
            print("Saving... [" + str(i) + " chunk]")
            i += 1
        print("File saved! [DONE]")

def SaveFileThread(name,src):
    thread = SaveThread(1, "Saving file", namef=name,  src=src)
    thread.start()


class SaveThread (threading.Thread):
   def __init__(self, threadID, name, namef, src):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.namef=namef
      self.src=src
   def run(self):
      print ("Starting " + self.name)
      SaveFile(namef=self.namef,  src=self.src)
      print ("Exiting " + self.name)