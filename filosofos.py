import time
import random
import threading

NUMERO_FILOSOFOS = 5
TIEMPO_TOTAL = 3

class filosofo(threading.Thread):
    sf = threading.Lock()
    status = [] 
    cola_tenedores = [] 
    count=0

    def __init__(self):
        super().__init__()    
        self.id=filosofo.count 
        filosofo.count+=1 
        filosofo.status.append('thinking') 
        filosofo.cola_tenedores.append(threading.Semaphore(0)) 
        print("El filosofo {0} Estado del filosofo = PENSANDO".format(self.id))

    def __del__(self):
        print("El filosofo {0} Estado del filosofo = Se levanta de la mesa".format(self.id))
    def pensar(self):
        time.sleep(random.randint(0,5)) 

    def derecha(self,i):
        return (i-1)%NUMERO_FILOSOFOS 

    def izquierda(self,i):
        return(i+1)%NUMERO_FILOSOFOS 

    def verificar(self,i):
        if filosofo.status[i] == 'HAMBRIENTO' and filosofo.status[self.izquierda(i)] != 'COMIENDO' and filosofo.status[self.derecha(i)] != 'COMIENDO':
            filosofo.status[i]='COMIENDO'
            filosofo.cola_tenedores[i].release()

    def tomar(self):
        filosofo.sf.acquire() 
        filosofo.status[self.id] = 'HAMBRIENTO'
        self.verificar(self.id) 
        filosofo.sf.release() 
        filosofo.cola_tenedores[self.id].acquire() 

    def soltar(self):
        filosofo.sf.acquire() 
        filosofo.status[self.id] = 'PENSANDO'
        self.verificar(self.izquierda(self.id))
        self.verificar(self.derecha(self.id))
        filosofo.sf.release() 

    def comer(self):
        print("El filosofo {} Comiendo".format(self.id))
        time.sleep(2) 
        print("El filosofo {} Ha terminado de comer".format(self.id))

    def run(self):
        for i in range(TIEMPO_TOTAL):
            self.pensar() 
            self.tomar() 
            self.comer() 
            self.soltar() 

def main():
    lista=[]
    for i in range(NUMERO_FILOSOFOS):
        lista.append(filosofo()) 

    for f in lista:
        f.start() 

    for f in lista:
        f.join() 

if __name__=="__main__":
    main()