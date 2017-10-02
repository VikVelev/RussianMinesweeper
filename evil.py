import psutil
import random
import numpy as np

def pidGenerator():
    
    numberProcs = 0
    for proc in psutil.process_iter():
        numberProcs += 1

    pidArray = np.empty(numberProcs, dtype=object) #filled with objects containing each rectangle
    i = 0; 
    for proc in psutil.process_iter():
        pidArray[i] = proc
        i += 1

    return pidArray[random.randint(0,pidArray.size)]

def showProcesses():
    for proc in psutil.process_iter():
        print(proc.name(),proc.pid)

def killProcess(pid):
    for proc in psutil.process_iter():
        if proc.pid == pid:
            print("Killed",proc.name())
            proc.kill()