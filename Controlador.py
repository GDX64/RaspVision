import queue


class ControladorPI:
    def __init__(self, P, I, fila = queue.Queue()):
        self.P=P
        self.I=I
        self.proporcional=0
        self.integral=0
        self.fila=fila

    def calc(self):
        referencia, leitura, tempo = self.fila.get()
        tempo = float(tempo)
        erro = referencia-leitura
        self.proporcional = self.P*erro
        self.integral += self.I*erro*tempo
        sinal=self.proporcional+self.integral
        return(float(sinal))
    
    def reset(self):
        self.proporcional=0
        self.integral=0
