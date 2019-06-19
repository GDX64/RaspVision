import cv2
import numpy as np
import time
from controladorPID import ControladorPID
import queue
import threading
from appThread import appThread
import ac
import sys

K_P = 0.10
K_I = 0.17
K_D = 0.10   #valores padrão

try:
    if len(sys.argv)==4:
        K_P=float(sys.argv[1])
        K_I=float(sys.argv[2])
        k_D=float(sys.argv[3])
        print("Valores PID: ", str(sys.argv[1:]))
    else:
        print("Usando valores padrão para o controlador")
except:
     print("coloca os valores direito, seu animal")
     raise
     sys.exit()


#estrutura

class IntVar():
    def __init__(self):
        self.valor=0
    
    def set(self, v):
        self.valor=v
    def get(self):
        return self.valor


#Streaming

fila1=queue.Queue(3)
myThread=appThread(1, "thread1", fila=fila1)
myThread.start()


#Controlador

fila = queue.Queue(20)


def comando(cpid):
    while True:
        w=cpid.calc()
        ac.motor(w,-w)
        print(w)
        

cpid = ControladorPID(K_P, K_I, K_D, fila)
thread1 = threading.Thread(target=comando, args=(cpid,))
thread1.start()

#Fim do controlador

lowHue = IntVar()
upHue = IntVar()
lowSat = IntVar()
upSat = IntVar()
lowBr = IntVar()
upBr = IntVar()

#Carregando configuracoes
        
def loadC(local):
    configuracao=open(local+'.txt','r')
    try:
        for nome in [upHue, upSat, upBr, lowHue, lowSat, lowBr]:
            nome.set(int(configuracao.readline().split()[0]))
    except:
        print("nao foi possivel carregar as configuracoes")

loadC('Config')

#inicializando o que precisa

cap = cv2.VideoCapture(0)

kernel = np.ones((10,10),np.uint8) #kernel do filtro

tempo=0
fps=0
tempo2=0
referencia=320

#funções

def fpsView(tempo, tempo2, fps):

    if tempo - tempo2 > 3:
        fps = int(1 / (time.time() - tempo))
        tempo2 = tempo

    tempo = time.time()
    return(fps, tempo, tempo2)


def filtro_de_cores(img, lower_color, upper_color):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_color, upper_color)
    return(cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel), mask)

def contornos(mask, img):

    image, contours, hierarchy = cv2.findContours(filt_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        maximo = 0
        for i in range(0, len(contours)):
            if len(contours[i]) > maximo:
                maximo = len(contours[i])
                index = i

        # img=cv2.drawContours(img, contours, -1, (0,0,255), 6)
        x, y, z, h = cv2.boundingRect(contours[index])
        cv2.rectangle(img, (x, y), (x + z, y + h), (0, 255, 0), 2)
        cv2.circle(img, (int(x + z / 2), int(y + h / 2)), 5, (255, 0, 0), -1)
        return(int(x + z / 2), int(y + h / 2)) #centro da figura
    except:
        print("Nenhum contorno encontrado")

while True:

    _, img = cap.read()

    lower_color = np.array([lowHue.get(), lowSat.get(), lowBr.get()])
    upper_color = np.array([upHue.get(), upSat.get(), upBr.get()])

    filt_mask, mask = filtro_de_cores(img, lower_color, upper_color)
    centro=contornos(filt_mask, img)
    
    #vendo os fps
    fps, tempo, tempo2 = fpsView(tempo, tempo2, fps)
    #mostra as imagens

    cv2.putText(img, 'FPS: {}'.format(fps), (0,450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2, cv2.LINE_AA)
    cv2.line(img,(320, 0),(320,480),(0,0,255),5)

    try:
        fila1.put(cv2.imencode('.jpg', img)[1].tobytes(), block=False)
    except queue.Full:
        print("Fila cheia")
    try:
        fila.put((referencia, centro[0], time.time()-tempo))
    except:
        print("Erro inesperado na fila")



cap.release()


    
    
    
    
    
    
    
    
    
    
