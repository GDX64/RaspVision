import queue


class ControladorPID:
    def __init__(self, P, I, D, fila = queue.Queue()):
        self.P=P
        self.I=I
        self.D=D
        self.proporcional=0
        self.integral=0
        self.derivativo=0
        self.fila=fila
        self.erroAnterior=0

    def calc(self):
        referencia, leitura, tempo = self.fila.get()
        erro = referencia-leitura
        self.derivativo = self.D*(erro-self.erroAnterior)/tempo
        self.proporcional = self.P*erro
        self.integral += self.I*erro*tempo
        sinal=self.proporcional+self.integral+self.derivativo

        self.erroAnterior=erro

        return(sinal)
    
    def reset(self):
        self.proporcional=0
        self.integral=0
        self.derivativo=0
        self.erroAnterior=0
