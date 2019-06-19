import RPi.GPIO as gpio
import time


# Disable warnings
gpio.setwarnings(False)

#Configuring GPIO
gpio.setmode(gpio.BCM) # gpio.setmode(gpio.BOARD) 
gpio.setup(17, gpio.OUT)
gpio.setup(27, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(19, gpio.OUT) 


#Configure the pwm objects and initialize its value
pwmE = gpio.PWM(16,1000)
pwmE.start(0)   
pwmD = gpio.PWM(19,1000)
pwmD.start(0)

#Velocidade maxima que o robo pode atingir
vMax = 1.0 # em m/s

# Inicializa as variaveis de duty cycle
MTA = 0
MTB = 0

#Loop infinite
while True:
    # Velocidades de referencia de cada roda 
    vE = 1 
    vD = 1  

    # Envia os valores de PWM para os motores
    pwmE.ChangeDutyCycle(MTA)
    pwmD.ChangeDutyCycle(MTB)    

    # Define os sentidos de giro das rodas
    if vE > 0:
        gpio.output(17, True)
        gpio.output(27, False)
    elif vE <= 0:
        vE = abs(vE)
        gpio.output(17, False)
        gpio.output(27, True)

    if vD > 0:
        gpio.output(22, False)
        gpio.output(23, True)
    elif vD <= 0:
        vD = abs(vD)
        gpio.output(22, True)
        gpio.output(23, False)


    #Create the dutycycle variables
    MTA = (int)((vE/vMax)*100)
    if MTA > 100:
        MTA = 100
    elif MTA < 0:
        MTA = 0
        
    MTB = (int)((vD/vMax)*100)
    if MTB > 100:
        MTB = 100
    elif MTB < 0:
        MTB = 0
        

#End code
gpio.cleanup()
exit()
    
